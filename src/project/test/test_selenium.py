import logging
import os
import tempfile
import time
from dataclasses import dataclass
from enum import Enum

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import mail
from django.test import override_settings
from django.urls import reverse
from django.utils.translation import gettext as _
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from apps.partners.models import Document, Project
from apps.users.models import User

logging.basicConfig(level=logging.INFO)


@dataclass
class SampleUser:
    name: str
    surnames: str
    email: str
    password: str
    email_verification_code: str
    email_verified: bool
    dni: str


class Strings(Enum):
    """
    Collect all the strings that you plan to use to find elements in the code
    that are susceptible to translation here.
    That way it will be easier to maintain the right version of the string
    whenever some text is changed.

    Also, during development we might only have english versions of the strings,
    but when applying the translations, all of them will need to be updated
    here.

    # IMPORTANT, ABOUT TRANSLATIONS:
    If you assert strings, i.e. like this:
        assert Strings.ADMIN_TITLE.value == self.selenium.title
    You need to be using 'gettext', NOT gettext_lazy.

    If for some reason you need to switch to gettext_lazy, these assertions will
    fail. In this case you should change all the assertions to something like
    this:
        assert str(Strings.ADMIN_TITLE.value) == self.selenium.title

    That way, the str() will force the resolution of the translation, instead of
    sending an object.

    """

    MENU_ADMIN = "Administration panel"
    ADMIN_TITLE = "Administració del lloc | Lloc administratiu de Django"
    LOGOUT = "Tancar sessió"
    HOME_TITLE = "Castellet Sostenible | Inici"
    PROFILE_TITLE = "Castellet Sostenible | Detalls del perfil"
    REGISTRY_UPDATE_TITLE = "Castellet Sostenible | Registre actualitzat"
    PASSWORD_CHANGE_TITLE = "Castellet Sostenible | Canvi de contrasenya"
    EMAIL_VALIDATION_TITLE = "Castellet Sostenible | Verificació del correu electrònic"
    NEWSLETTER_TITLE = "Castellet Sostenible | Newsletter"
    NEWSLETTER_SUCCESS_TITLE = "Castellet Sostenible | Alta al butlletí completada"
    DOCUMENTS_TITLE = "Castellet Sostenible | Documents"


@override_settings(
    ALLOWED_HOSTS=["*"],
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage",
    POST_OFFICE={
        "BACKENDS": {
            "default": "django.core.mail.backends.locmem.EmailBackend",
        },
        "DEFAULT_PRIORITY": "now",
    },
)
class MySeleniumTests(StaticLiveServerTestCase):
    """
    STATICFILES_STORAGE + StaticLiveServerTestCase vs LiveServerTestCase:
    Just using LiveServerTestCase it will not work because the tests run with
    debug disabled, meaning that it will trigger Whitenoise's static files
    indexation.
    For that to work, the static files need to be there, therefore, the tests
    will only work if you run `collectstatic` before running the tests.

    We can avoid Whitenoise to crash by overriding the setting STATICFILES_STORAGE
    to the default that Django uses.

    But then, Django will still try to serve the static files, so we need to
    extend StaticLiveServerTestCase because this class overrides the static
    serving behaviour to do the same that it does with DEBUG enabled - that is,
    to serve the files without any need to `collectstatic` first.
    """

    host = "castellet-app"
    # Uncomment this code if you want Selenium to connect to the actual web
    # service instead of the test one. Is assuming that Gunicorn is starting
    # it at the port 8000, because you have to use the internal port and
    # not the one that Docker is exposing outside.
    #
    # Beware that Selenium will be using the database in the state that you
    # have it now, but those tests are designed to work only with a fresh
    # database, and also that the override_settings is only affecting the test
    # server that you will not be using.
    # live_server_url = 'http://{}:8000'.format(
    #     socket.gethostbyname(socket.gethostname())
    # )
    obj_user1 = None
    obj_user2 = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set up the Selenium WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")  # Disable sandboxing for Docker
        cls.selenium = webdriver.Remote(
            command_executor="http://castellet-selenium:4444/wd/hub", options=options
        )
        cls.selenium.implicitly_wait(10)  # Set implicit wait time
        cls.sample_data = {
            "first_user": SampleUser(
                name="Andrew",
                surnames="McTest",
                email="andrew@codi.coop",
                dni="12345678A",
                password="0pl#9okm8ijn",
                email_verification_code="1234",
                email_verified=False,
            ),
        }

    @classmethod
    def tearDownClass(cls):
        # Close the Selenium WebDriver
        cls.selenium.quit()
        super().tearDownClass()

    def reverse_absolute_url(self, reverse_string):
        return self.absolute_url_of_path(reverse(reverse_string))

    def absolute_url_of_path(self, path):
        return f"{self.live_server_url}{path}"

    def burger_menu_action(self):
        burger_menu = self.selenium.find_element(
            By.ID,
            "burger_button",
        )
        burger_menu.click()

    def logging_url_title_and_assert_title(self, title=None):
        logging.info(f"Opened: {self.selenium.current_url}")
        logging.info(f"Title: {self.selenium.title}")
        assert title == self.selenium.title

    def create_file(self, filename, content):
        with tempfile.TemporaryDirectory() as tempdir:
            tmpfilepath = os.path.join(tempdir, f"{filename}.pdf")
            with open(tmpfilepath, "w") as tmpfile:
                tmpfile.write(content)
        return filename

    def _check_mail_sent(self, recipient, string_in_body=""):
        """
        During the test, every time an email is sent it gets added to
        mail.outbox.
        This makes it difficult to test whether a specific email is sent or not.

        Instructions to test the emails

        If there's 1 email sent and pending to be tested:
        - Call this method normally.
        - After that, the email will be removed from the outbox, so you cannot
        test it a second time.

        If there's more than 1 email:
        - Call this method as many times as emails are pending to be tested.
        - In each call, the email in the index 0 of the outbox will be tested
        and removed from the outbox. So the different calls to this method will
        need to be done in the same order as the emails were sent.
        """
        self.assertGreaterEqual(len(mail.outbox), 1)
        current_mail = mail.outbox.pop(0)
        # The mail's "to" property is a list, as it can be sent to multiple
        # recipients at once. We are only testing for one.
        self.assertIn(recipient, current_mail.to)
        logging.info(f"Checked: Sent email to {recipient}")
        self.assertIn(string_in_body, current_mail.body)
        logging.info(f'Checked: "{string_in_body}" present in email body')

    def click_non_interactable_element(self, element):
        # Checkboxes are not rendered as is, but hidden by CSS and replaced with
        # other elements, with the purpose of styling them better.
        # Because of that, you cannot send a click() or interact with the
        # checkbox directly from Selenium; it'll throw the error:
        # selenium.common.exceptions.ElementNotInteractableException: Message:
        # element not interactable
        # The simplest solution is to send the click via JS:
        self.selenium.execute_script("arguments[0].click();", element)

    def select_element_by_text(self, text):
        """
        Select an element by its text
        """
        elements = self.selenium.find_elements(
            By.XPATH,
            f"//*[contains(text(), '{text}')]",
        )
        return elements[0] if elements else None

    def test_selenium(self):
        """
        Selenium tests controller

        We need the Selenium flow to follow a specific order, because each action
        will probably depend on the data and changes produced by previous ones.

        If we do that in different tests, we cannot ensure this order and also
        the principle is to make tests that are standalone.

        Because of that, we're using a single test method and splitting it
        in other private methods to make it more organized.
        """

        # Preparations
        self._resize()

        # Fer login amb el compte d'admin que crea per defecte.
        # Verifica que al menú de l'app apareix el botó per anar a l'admin.
        self._admin_login()
        logging.info("Test Login finished.")

        self._verify_email()
        logging.info("Test Verify email finished.")

        self._password_change()
        logging.info("Test Password change finished.")

        self._home()
        logging.info("Test Home finished.")

        self._newsletter()
        logging.info("Test Newsletter finished.")

        self._documents()
        logging.info("Test Documents finished.")

        logging.info("#####################################")
        logging.info("#### All tests Selenium finished ####")
        logging.info("#####################################")

    def _resize(self):
        """
        Elements need to be in viewport to be interactable.
        For instance, we cannot send a click() to a checkbox if it's not
        visible, so we either resize the browser window to make everything
        visible or we have to be scrolling to each element when that happens.
        """
        self.selenium.get(self.live_server_url)
        logging.info(f"Opened: {self.live_server_url}")
        logging.info(f"Title: {self.selenium.title}")
        self.selenium.set_window_size(500, 2000)

    def _login(self, user, password):
        self.selenium.get(self.live_server_url)
        # The home page will probably be the login page, but to make sure that
        # we reach the login page, we open de burger menu and navigate to
        # sign-in.
        self.burger_menu_action()
        login_menu_option = self.selenium.find_element(By.ID, "menu_login")
        login_menu_option.click()
        logging.info(f"Opened: {self.selenium.current_url}")
        logging.info(f"Title: {self.selenium.title}")

        login_user = self.selenium.find_element(By.ID, "id_username")
        login_password = self.selenium.find_element(By.ID, "id_password")

        login_user.send_keys(user)
        login_password.send_keys(password)
        login_password.send_keys(Keys.RETURN)

    def _admin_login(self):
        self._login(
            settings.DJANGO_SUPERUSER_EMAIL,
            settings.DJANGO_SUPERUSER_PASSWORD,
        )
        self.burger_menu_action()
        admin_menu = self.selenium.find_element(By.ID, "menu_admin")
        admin_menu.click()

        self.logging_url_title_and_assert_title(Strings.ADMIN_TITLE.value)
        logging.info("Logged in to admin with initial superuser.")

    def _verify_email(self):
        # self.logging_url_title_and_assert_title(Strings.PROFILE_TITLE.value)
        # Verify email
        button_alert = self.selenium.find_element(By.ID, "id_verify_email")
        button_alert.click()

        self.logging_url_title_and_assert_title(Strings.EMAIL_VALIDATION_TITLE.value)

        # Click on the button to send the verification email.
        send_button = self.selenium.find_element(By.ID, "id_submit")
        send_button.click()

        # Wait for the verification email to be sent.
        self._check_mail_sent(
            self.sample_data["first_user"].email,
            self.sample_data["first_user"].name,
        )
        verification_code = self.selenium.find_element(
            By.ID, "id_email_verification_code"
        )
        self.user = User.objects.filter(
            email=self.sample_data["first_user"].email
        ).first()
        verification_code.send_keys(self.user.email_verification_code)
        verification_code.send_keys(Keys.RETURN)
        # Template confirm account has been successfully verified.
        # Click on the button Go Back.
        logging.info("Verified email.")

        go_back = self.select_element_by_text(_("Go back"))
        go_back.click()

    def _update_profile(self):
        # Back to profile page.
        self.logging_url_title_and_assert_title(Strings.PROFILE_TITLE.value)

        update_name = self.selenium.find_element(By.ID, "id_name")
        update_surnames = self.selenium.find_element(By.ID, "id_surnames")

        # Update the profile | Name & Surnames.
        update_name.clear()
        update_surnames.clear()
        update_name.send_keys("Andrews")
        update_surnames.send_keys("McDolls")

        update_surnames.send_keys(Keys.RETURN)

        self.logging_url_title_and_assert_title(Strings.REGISTRY_UPDATE_TITLE.value)

        button_back = self.selenium.find_element(By.ID, "id_back")
        button_back.click()

        self.logging_url_title_and_assert_title(Strings.PROFILE_TITLE.value)

        # Update the profile | Email.
        update_email = self.selenium.find_element(By.ID, "id_email")
        update_email.clear()
        update_email.send_keys("andrews.mcdolls@gmail.com")
        self.user.email = "andrews.mcdolls@gmail.com"
        self.user.save()
        update_email.send_keys(Keys.RETURN)

        self.logging_url_title_and_assert_title(Strings.REGISTRY_UPDATE_TITLE.value)

        button_back = self.selenium.find_element(By.ID, "id_back")
        button_back.click()

        # Verify again the e-mail again after changing it
        button_alert = self.selenium.find_element(By.ID, "id_verify_email")
        button_alert.click()

        self.logging_url_title_and_assert_title(Strings.EMAIL_VALIDATION_TITLE.value)

        # Click on the button to send the verification email.
        send_button = self.selenium.find_element(By.ID, "id_submit")
        send_button.click()
        verification_code = self.selenium.find_element(
            By.ID, "id_email_verification_code"
        )
        code = (
            User.objects.filter(email=self.user.email).first().email_verification_code
        )
        verification_code.send_keys(code)
        verification_code.send_keys(Keys.RETURN)
        # Template confirm account has been successfully verified.
        # Click on the button Go Back.
        logging.info("Verified email.")

        go_back = self.select_element_by_text(_("Enrere"))
        go_back.click()

    def _password_change(self):
        self.logging_url_title_and_assert_title(Strings.PROFILE_TITLE.value)

        # Change password.
        button_password_change = self.selenium.find_element(By.ID, "id_password_change")
        button_password_change.click()

        self.logging_url_title_and_assert_title(Strings.PASSWORD_CHANGE_TITLE.value)

        old_password = self.selenium.find_element(By.ID, "id_old_password")
        old_password.send_keys(self.sample_data["first_user"].password)
        new_password = self.selenium.find_element(By.ID, "id_new_password1")
        new_password.send_keys("0pl#4jT7m8ijn")
        password_confirmation = self.selenium.find_element(By.ID, "id_new_password2")
        password_confirmation.send_keys("0pl#4jT7m8ijn")
        password_confirmation.send_keys(Keys.RETURN)

        self.logging_url_title_and_assert_title(Strings.PASSWORD_CHANGE_TITLE.value)

        # Click on the button Go Back.
        go_back = self.selenium.find_element(By.ID, "id_back")
        go_back.click()

        self.logging_url_title_and_assert_title(Strings.PROFILE_TITLE.value)

    def _home(self):
        # Open the partners menu to select the Home option.
        self.burger_menu_action()
        home_menu_option = self.selenium.find_element(By.ID, "menu_home")
        home_menu_option.click()

        self.logging_url_title_and_assert_title(Strings.HOME_TITLE.value)

    def _newsletter(self):
        # Click on the link Subscribe to Newsletter.
        newsletter_option = self.selenium.find_element(By.ID, "id_newsletter")
        newsletter_option.click()

        self.logging_url_title_and_assert_title(Strings.NEWSLETTER_TITLE.value)

        name = self.selenium.find_element(By.ID, "id_name")
        surnames = self.selenium.find_element(By.ID, "id_surnames")
        email = self.selenium.find_element(By.ID, "id_email")

        name.send_keys(self.sample_data["first_user"].name)
        surnames.send_keys(self.sample_data["first_user"].surnames)
        email.send_keys(self.sample_data["first_user"].email)
        email.send_keys(Keys.RETURN)

        # Test mailing to the user confirming the success of their subscription
        self._check_mail_sent("andrews.mcdolls@gmail.com")

        self.logging_url_title_and_assert_title(Strings.NEWSLETTER_SUCCESS_TITLE.value)

        # Click on the button Go Back.
        button_back = self.selenium.find_element(By.ID, "id_back")
        button_back.click()

        self.logging_url_title_and_assert_title(Strings.HOME_TITLE.value)

    def _documents(self):
        # Create new projects
        project_1 = Project.objects.create(name="Mock project 1")
        project_2 = Project.objects.create(name="Mock project 2")

        # Create new documents
        Document.objects.create(
            project=project_1,
            title="Mock document 1",
            file=self.create_file("Mock_file_1.pdf", "Test file content"),
        )
        Document.objects.create(
            project=project_2,
            title="Mock document 2",
            file=self.create_file("Mock_file_2.pdf", "Test file content"),
        )

        # Open the partners menu to select the Documents option.
        self.burger_menu_action()
        documents_menu_option = self.selenium.find_element(By.ID, "menu_documents")
        documents_menu_option.click()
        self.logging_url_title_and_assert_title(Strings.DOCUMENTS_TITLE.value)

        # Click on the button to select document 1
        document = self.selenium.find_element(By.ID, "id_document_1")
        document.click()

        # Click on the button to select document 2
        document = self.selenium.find_element(By.ID, "id_document_2")
        document.click()

        # Click on the button to filter document by project
        document = self.selenium.find_element(By.ID, "dropdownDefault")
        document.click()

        # Click on the checkbox to select project 1
        document = self.selenium.find_element(By.ID, "1")
        document.click()

        # Pause to facilitate the process
        time.sleep(1)

        # Click on the button to select document 1
        document = self.selenium.find_element(By.ID, "id_document_1")
        document.click()

        # Click on the button to filter document by project
        document = self.selenium.find_element(By.ID, "dropdownDefault")
        document.click()

        # Click on the checkbox to deselect project 1
        document = self.selenium.find_element(By.ID, "1")
        document.click()

        # Click on the checkbox to select project 2
        document = self.selenium.find_element(By.ID, "2")
        document.click()

        # Pause to facilitate the process
        time.sleep(1)

        # Click on the button to select document 2
        document = self.selenium.find_element(By.ID, "id_document_2")
        document.click()

        # Click on the button to filter document by project
        document = self.selenium.find_element(By.ID, "dropdownDefault")
        document.click()

        # Click on the button to deselect document 2
        document = self.selenium.find_element(By.ID, "2")
        document.click()

        # Click on the button to select document 1
        document = self.selenium.find_element(By.ID, "id_document_1")
        document.click()

        # Click on the button to select document 2
        document = self.selenium.find_element(By.ID, "id_document_2")
        document.click()

        # Click on the breadcrumb to go Homepage
        breadcrumb_home_option = self.selenium.find_element(By.ID, "id_home")
        breadcrumb_home_option.click()
        self.logging_url_title_and_assert_title(Strings.HOME_TITLE.value)
