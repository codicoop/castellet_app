from django.utils import formats, timezone

from project.post_office import send


def send_confirmation_newsletter(subscriber):
    context = {
        "user_name": subscriber["name"],
        "date": str(
            formats.date_format(
                timezone.now().date(),
                format="SHORT_DATE_FORMAT",
                use_l10n=True,
            )
        ),
        "time": str(formats.time_format(timezone.localtime(timezone.now()).time())),
        "user_email": subscriber["email"],
    }
    send(
        recipients=[
            subscriber["email"],
        ],
        template="newsletter",
        context=context,
    )
