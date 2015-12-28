from django.test import TestCase, Client
from django.contrib.auth.models import User


class TestPageLoad(TestCase):

    def _assert_templates_used(self, response, templates_expected):
        templates_used = []

        for template in response.templates:
            templates_used.append(template.name)

        self.assertListEqual(templates_used, templates_expected)

    def setUp(self):
        self.user1 = User.objects.create_user(username='john', email='test@test.pl', password='pass',
                                             first_name='John', last_name='Doe')

        self.user1_pk = self.user1.pk

    def test_login_status(self):
        client = Client()
        response = client.get('/accounts/login', follow=True)

        self.assertEquals(response.status_code, 200)

    def test_login_templates(self):
        client = Client()
        response = client.get('/accounts/login', follow=True)

        templates_expected = ['registration/login.html', 'describe/base.html']
        self._assert_templates_used(response, templates_expected)

    def test_logout_status(self):
        client = Client()
        response = client.get('/logout', follow=True)

        self.assertEquals(response.status_code, 200)

    def test_logout_templates(self):
        client = Client()
        response = client.get('/logout', follow=True)

        templates_expected = ['registration/login.html', 'describe/base.html']
        self._assert_templates_used(response, templates_expected)

    def test_not_authorized(self):
        client = Client()
        response = client.get('/', follow=True)

        self.assertSequenceEqual(response.redirect_chain, [('/accounts/login/?next=/', 302)])

    def test_authorized(self):
        client = Client()
        client.login(username="john", password="pass")
        response = client.get('/', follow=True)

        templates_expected = ['describe/main_page.html', 'describe/base.html']
        self._assert_templates_used(response, templates_expected)