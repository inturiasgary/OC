from django.test import TestCase
from django.db import IntegrityError
from links.models import Link, Category

class CreateCategoryTest(TestCase):
    def test_fail_create_category_with_already_existent_title(self):
        """
        Tests that an attempt to create a category with an already existent title fails.
        """
        Category.objects.create(title="Category A", description="This is the category a's description")
        self.assertRaises(IntegrityError, Category.objects.create, title="Category A", description="another description")


class ModifyCategoryTest(TestCase):
    def test_fail_attempt_change_title_to_already_existent(self):
        """
        Tests that an attempt to modify a category with an already existent title fails.
        """
        Category.objects.create(title="Category A", description="description")
        a_category = Category.objects.create(title="Category B", description="This is a description for category B")
        a_category.title = "Category A"
        self.assertRaises(IntegrityError, a_category.save)


class CreateLinkTest(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(title="Category 1", description="A Description")

    def test_url_attribute_has_to_be_unique(self):
        """
        Tests that a link's url has to be unique.
        """
        link_a = Link.objects.create(title="Link A", description="Description A", url="www.google.com", category=self.category1)
        self.assertRaises(IntegrityError, Link.objects.create, title="Another title", url=link_a.url, category=self.category1)


class ModifyLinkTest(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(title="Category 1", description="A Description")

    def test_fail_attempt_change_url_to_another_existent(self):
        """
        Tests that a link's url has to be unique.
        """
        link_a = Link.objects.create(title="Link A", description="Description A", url="www.google.com", category=self.category1)
        link_b = Link.objects.create(title="Link B", description="Description B", url="www.amazon.com", category=self.category1)
        link_b.url = link_a.url
        self.assertRaises(IntegrityError, link_b.save)

