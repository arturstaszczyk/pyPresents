from django.test import TestCase
from django.contrib.auth.models import User, Group
from describe.exceptions import CannotFindReceiver
from describe.persons_controller import PersonsController
from describe.models import RandomizationModel

class TestRandomizer (TestCase):

    def setUp(self):
        self.me = User.objects.create_user(username='jonh', email="john@example.com", password='pass',
                                 first_name='John', last_name="Doe")

    def _add_one_more_user(self):
        self.user1 = User.objects.create_user(username='max', email="max@example.com", password='pass',
                         first_name='Max', last_name = "Mustermann")

    def _add_two_more_users(self):
        self.user1 = User.objects.create_user(username='max', email="max@example.com", password='pass',
                         first_name='Max', last_name="Mustermann")

        self.user2 = User.objects.create_user(username='jan', email="jan@example.com", password='pass',
                                 first_name='Jan', last_name="Kowalski")

    def _create_test_group(self):
        self.group = Group()
        self.group.name = 'test'
        self.group.save()

    def _add_group_to_user(self, user, group):
        group.user_set.add(user)
        group.save()


    def test_create_persons(self):
        self._add_two_more_users()
        persons = PersonsController()

        person1 = persons.create(self.me)
        self.assertEquals(person1.get_user_name(), "John Doe")

    def test_getrandom(self):
        self._add_two_more_users()

        persons = PersonsController()

        for x in range(1000):
            person = persons.get_rand_user_not_me(self.me)
            self.assertNotEqual(person.pk, self.me.pk)

    def test_getrandom_exception(self):
        persons = PersonsController()
        self.assertRaises(RuntimeError, persons.get_rand_user_not_me, self.me)

    def test_draw_error_no_receiver(self):
        persons = PersonsController()
        self.assertRaises(CannotFindReceiver, persons.draw, self.me)

    def test_draw_error_one_group(self):
        self._create_test_group()
        self._add_one_more_user()

        self._add_group_to_user(self.me, self.group)
        self._add_group_to_user(self.user1, self.group)

        persons = PersonsController()
        self.assertRaises(CannotFindReceiver, persons.draw, self.me)


    def test_draw_no_group(self):
        self._add_one_more_user()

        persons = PersonsController()
        persons.draw(self.me)

        self.assertEquals(len(RandomizationModel.objects.all()), 1)

        relationship = RandomizationModel.objects.get(user_id=self.me.pk)
        self.assertEquals(str(relationship), "John Doe -> Max Mustermann")

