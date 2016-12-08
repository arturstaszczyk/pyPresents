from django.contrib.auth.models import User
from django.test import TestCase
from describe.models import PersonModel, RandomizationModel
from describe.controllers.display_controller import DisplayController

class TestDisplayController (TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='max', email="max@example.com", password='pass',
                                              first_name='Max', last_name="Mustermann")

        self.user1.save()

        self.user2 = User.objects.create_user(username='jan', email="jan@example.com", password='pass',
                                              first_name='Jan', last_name="Kowalski")
        self.user2.save()

        person1 = PersonModel(user_id = self.user1)
        person1.save()

        person2 = PersonModel(user_id = self.user2)
        person2.save()

    def tearDown(self):
        PersonModel.objects.all().delete()
        RandomizationModel.objects.all().delete()


    def test_should_not_display_edit_field1(self):

        displayController = DisplayController()
        self.assertNotEquals(displayController.can_user_describe_present(), True)


    def test_should_display_edit_field1(self):
        displayController = DisplayController()

        randomization = RandomizationModel(user_id=self.user1.pk, giving_id=self.user2.pk)
        randomization.save()
        randomization = RandomizationModel(user_id=self.user2.pk, giving_id=self.user1.pk)
        randomization.save()

        self.assertEquals(displayController.can_user_describe_present(), True)

    def test_should_not_display_edit_field2(self):
        displayController = DisplayController()

        randomization = RandomizationModel(user_id=self.user1.pk, giving_id=self.user2.pk)
        randomization.save()

        self.assertEquals(displayController.can_user_describe_present(), False)
