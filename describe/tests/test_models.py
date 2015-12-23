from django.test import TestCase
from django.contrib.auth.models import User
from describe.models import PersonModel, RandomizationModel

class TestModels(TestCase):

    def _create_person_model(self, user):
        person = PersonModel()
        person.user_id = user
        return person

    def _create_randomization_model(self, user1, user2):
        rand_model = RandomizationModel()
        rand_model.user_id = user1.pk
        rand_model.giving_id = user2.pk
        return rand_model

    def setUp(self):
        self.user1 = User.objects.create_user(username='john', email='test@test.pl', password='pass',
                                             first_name='John', last_name='Doe')

        self.user2 = User.objects.create_user(username='jan', email='test@test.pl', password='pass',
                                             first_name='Jan', last_name='Kowalski')

    def test_person_model(self):

        person = self._create_person_model(self.user1)

        self.assertEquals(person.present_desc(), "")
        self.assertEquals(person.get_user_name(), "John Doe")
        self.assertEquals(str(person), "John Doe")

    def test_person_model_cmp_ne(self):
        person1 = self._create_person_model(self.user1)
        person2 = self._create_person_model(self.user2)

        self.assertNotEqual(person1, person2)

    def test_person_model_cmp_eq(self):
        person1 = self._create_person_model(self.user1)
        person2 = self._create_person_model(self.user1)

        self.assertEqual(person1, person2)

    def test_randomization_model(self):
        rand_model = self._create_randomization_model(self.user1, self.user2)

        self.assertEquals(str(rand_model), self.user1.first_name + " " + self.user1.last_name + " -> " +
                                                self.user2.first_name + " " + self.user2.last_name)
