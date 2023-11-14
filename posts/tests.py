from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import AnonymousUser
from users.models import User
from . import views
from .models import Post

# Create your tests here.


class IndexPageTest(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("post:index"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("post:index"))
        self.assertTemplateUsed(response, "index.html")

    def test_search_forms(self):
        response = self.client.post(
            reverse("post:index"),
            {"title": "Testing"},
            content_type="application/x-www-form-urlencoded",
        )
        # self.assertEqual(response.get("title"),"Testing")
        self.assertEqual(response.status_code, 200)


class ReadPostTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        user = User.objects.create(
            username="testing",
            email="testing@test.tst",
        )
        user.set_password("pda2oraora##")
        user.save()
        self.user = user

        Post.objects.create(
            title="Testing",
            content="Lorem ipsum dolor sit amet",
            summary="Lorem ipsum dolor sit amet",
            author=self.user,
            is_draft=False,
            is_complete=False,
        )
        Post.objects.create(
            title="Testing draft post",
            content="Lorem ipsum dolor sit amet",
            summary="Lorem ipsum dolor sit amet",
            author=self.user,
            is_draft=True,
            is_complete=False,
        )

    def test_url_available_by_name(self):
        response = self.client.get(
            reverse("post:read", kwargs={"id": 1, "title": "testing"})
        )
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        self.client.login(username="testing", password="pda2oraora##")
        response = self.client.get(
            reverse("post:read", kwargs={"id": 1, "title": "testing"})
        )
        self.assertTemplateUsed(response, "read.html")

    def test_page_not_found_if_user_is_not_the_author(self):
        response = self.client.get(
            reverse(
                "post:read",
                kwargs={"id": 2, "title": slugify("Testing draft post")},
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_page_found_if_user_is_the_author(self):
        self.client.login(username="testing", password="pda2oraora##")
        response = self.client.get(
            reverse(
                "post:read",
                kwargs={"id": 2, "title": slugify("Testing draft post")},
            )
        )

        self.assertEqual(response.status_code, 200)


class TestCreatePostPage(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.confirm_user = User.objects.create(
            username="testing",
            email="testing@test.tst",
            password="pda2oraora##",
            account_confirmed=True,
        )
        self.confirm_user.set_password("pda2oraora##")
        self.confirm_user.save()

        self.unconfirm_user = User.objects.create(
            username="testingggg",
            email="testing@test.testing",
            password="pda2oraora##",
            account_confirmed=False,
        )
        self.unconfirm_user.set_password("pda2oraora##")
        self.unconfirm_user.save()

    def test_url_available_by_name(self):
        self.client.login(username="testing", password="pda2oraora##")
        response = self.client.get(reverse("post:create"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        self.client.login(username="testing", password="pda2oraora##")
        response = self.client.get(reverse("post:create"))
        self.assertTemplateUsed(response, "create.html")
