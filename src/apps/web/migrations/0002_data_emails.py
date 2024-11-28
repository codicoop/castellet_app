from django.db import migrations

from project.post_office import textify


def populate_mail_templates(apps, schema_editor):
    mail_model = apps.get_model("post_office", "EmailTemplate")

    templates = [
        dict(
            id="newsletter",
            translated_templates={
                "en": {
                    "subject": "Successfully subscribed to Castellet Sostenible's newsletter",
                    "body": """
    <p>Hello, {{user_name}},</p>
    <p>We're sending you this e-mail because today {{date}} at {{time}}
    your subscription to our newsletter has been completed with your email address
    {{user_email}}.</p>
    <p>From now on we will keep you informed with all our news.</p>
    <p>Thank you for being part of our community.</p>
                        """,
                },
                "ca": {
                    "subject": "Confirmació d'alta al butlletí de Castellet Sostenible",
                    "body": """
    <p>Hola, {{user_name}},</p>
    <p>T'enviem aquest correu perquè avui {{date}} a les {{time}}
    s'ha completat la teva subscripció a nostra newsletter amb el teu correu electrònic
    {{user_email}}.</p>
     <p>D'ara endavant et mantindrem informat amb totes les nostres novetats.</p>
     <p>Gràcies per formar part de la nostra comunitat.</p>
                        """,
                },
            },
        ),
    ]

    print("")
    for template in templates:
        obj, created = mail_model.objects.update_or_create(
            name=template.get("id"),
            defaults={
                "name": template.get("id"),
            },
        )
        for lang, translated_template in template.get("translated_templates").items():
            obj.translated_templates.create(
                language=lang,
                subject=translated_template.get("subject"),
                html_content=translated_template.get("body"),
                content=textify(translated_template.get("body")),
                # name field included due this bug:
                # https://github.com/ui/django-post_office/issues/214
                name=template.get("id"),
            )


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0001_initial"),
        ("post_office", "__latest__"),
    ]

    operations = [
        migrations.RunPython(populate_mail_templates),
    ]
