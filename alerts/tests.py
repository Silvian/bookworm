"""Alerts app feature tests."""
from unittest.mock import patch

from django.test import TestCase

from alerts import tasks
from alerts.models import SMSAlert
from books.models import Profile
from books.tests import ReadingListFactory, UserFactory


class TestSMSAlertTaskTestCase(TestCase):
    """Test the sms alert task test case."""

    @classmethod
    def setUpTestData(cls):
        cls.sms_alert = SMSAlert.objects.create(send_alert=True)
        cls.user = UserFactory(is_superuser=True)
        cls.reading_list = ReadingListFactory(
            started_reading=True,
            finished_reading=False,
            user=cls.user,
        )

    @patch("alerts.services.SMSService.send_alert")
    def test_send_sms_alert_task(self, send_alert_mock):
        """Test send sms alert task."""
        # Ensure user profile contains the expected data
        profile = Profile.objects.get(user=self.user)
        profile.mobile_number = "+441234567890"
        profile.save()

        # Expected message
        message = "{} {}".format(self.sms_alert.message, self.reading_list.book.title)

        # Trigger the sms alerts task
        tasks.send_sms_alert()

        send_alert_mock.assert_called_once_with(
            message=message,
            mobile=profile.mobile_number,
        )
