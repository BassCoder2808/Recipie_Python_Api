from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTests(TestCase):

    def setUp(self):

        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(email= 'vedantjolly2001@gmail.com',password= 'BassCoder2808')

        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(email= 'vedant.jolly@spit.ac.in',password= 'BassCoder2808',name= 'BassCoder2808')

    def test_users_listed(self):
        """Test that users are listed in our application"""

        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the edit user page is rendered correctly"""

        url = reverse('admin:core_user_change',args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code,200)

    def test_create_user_page(self):
        """Test that the create user page is rendered correctly"""

        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code,200)
