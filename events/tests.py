from django.test import TestCase
from datetime import datetime
from opendoor.apps.events.models import Event

from django.contrib.auth.models import User

class CreateEventTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='event_owner')
        self.event1=Event(
                start_date=datetime(2010, 1, 1),
                end_date=datetime(2010, 1, 1),
                title="test title1",
                excerpt="test excerpt1",
                description="test description1",
                published=True,
                publish_on=datetime(2009,12,13),
                icon="/home/gary/UBUNTU.bmp",
                registered=datetime(2009,12,12),
                user=self.user
        )
        self.event1.save()

    def test_fail(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        pass
