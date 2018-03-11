"""Alerts tasks."""

from celery.utils.log import get_task_logger

from alerts.models import SMSAlert
from alerts.services import SMSService
from books.models import ReadingList
from bookworm.celery import app

logger = get_task_logger(__name__)


@app.task
def send_sms_alert():
    """Send sms alerts task."""
    service = SMSService()
    alert = SMSAlert.load()

    if alert.send_alert:
        reading_list = ReadingList.objects.all()

        for book in reading_list:
            if book.started_reading and not book.finished_reading:
                service.send_alert(
                    message="{} {}".format(
                        alert.message,
                        book.book.title,
                    ),
                    mobile=book.user.profile.mobile_number,
                )
