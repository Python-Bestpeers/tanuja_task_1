from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Task


class TaskCreateViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="user1@gmail.com", password="user1234"
        )
        self.user2 = User.objects.create_user(
            email="user2@gmail.com", password="user78234"
        )
        self.client.login(email="user1@gmail.com", password="user1234")
        self.url = reverse("TaskCreate")

    def test_task_create_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taskcreateform.html")

    def test_task_create_post(self):
        data = {
            "title": "Test Task",
            "priority": "high",
            "status": "pending",
            "end_date": "2023-12-31",
            "assigned_to": self.user2.id,
            "description": "This is a test task.",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title="Test Task").exists())
        self.assertRedirects(response, reverse("homepage"))


class TaskUpdateViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="user@gmail.com", password="user123"
        )
        self.user2 = User.objects.create_user(
            email="user2@gmail.com", password="user78234"
        )
        self.task = Task.objects.create(
            title="Initial Task",
            priority="medium",
            status="pending",
            end_date="2023-12-31",
            assigned_to=self.user2,
            description="Initial Description",
            assigned_by=self.user,
        )
        self.client.login(email="user@gmail.com", password="user123")
        self.url = reverse("UpdateTask", args=[self.task.id])

    def test_task_update_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "updateform.html")

    def test_task_update_view_post_success(self):
        data = {
            "title": "Updated Task",
            "priority": "high",
            "status": "in-progress",
            "end_date": "2023-12-31",
            "description": "Updated Description",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Task")
        self.assertEqual(self.task.priority, "high")
        self.assertEqual(self.task.status, "in-progress")
        self.assertEqual(self.task.description, "Updated Description")
        self.assertRedirects(response, reverse("homepage"))


class DeleteTaskTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="testuser@gmail.com", password="testpass"
        )
        self.user2 = User.objects.create_superuser(
            email="admin@example.com", password="adminpass"
        )

        self.task = Task.objects.create(
            title="Task to be deleted",
            description="This task will be deleted in the test",
            assigned_to=self.user,
            assigned_by=self.user2,
            end_date="2024-12-26",
            status="pending",
            priority="medium",
        )

    def test_delete_task(self):
        self.client.login(email="testuser@gmail.com", password="testpass")
        response = self.client.get(
            reverse("DeleteTask", kwargs={"id": self.task.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())


class TaskSearchTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@gmail.com", password="password"
        )
        self.user2 = User.objects.create_superuser(
            email="admin@example.com", password="adminpass"
        )
        self.task = Task.objects.create(
            title="Task to be deleted",
            description="This task will be deleted in the test",
            assigned_to=self.user,
            assigned_by=self.user2,
            end_date="2024-12-25",
            status="pending",
            priority="medium",
        )
        self.task1 = Task.objects.create(
            title="Complete Django Project",
            description="This task will be deleted in the test",
            assigned_to=self.user,
            assigned_by=self.user2,
            end_date="2024-12-24",
            status="pending",
            priority="medium",
        )
        self.task2 = Task.objects.create(
            title="Task to be deleted",
            description="Complete Django Project",
            assigned_to=self.user,
            assigned_by=self.user2,
            end_date="2024-12-23",
            status="pending",
            priority="medium",
        )

    def test_search_results(self):
        self.client.login(email="testuser@gmail.com", password="password")
        response = self.client.get(reverse("TaskSearch"), {"q": "Complete"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Complete Django Project")
        self.assertNotContains(response, "Learn Testing")


class LogoutPageTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpass"
        )

    def test_logout_page(self):
        self.client.login(email="testuser@example.com", password="testpass")
        response = self.client.get(reverse("logoutpage"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("loginform"))
        response = self.client.get(reverse("homepage"))
        self.assertNotEqual(response.status_code, 200)


class ProfileViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpass123"
        )

    def test_profile_view_exists(self):
        self.client.login(email="testuser@example.com", password="testpass123")
        response = self.client.get(reverse("profileview"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "userprofile.html")
        self.assertContains(response, "testuser@example.com")


class TestAllTaskView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="testuser@gmail.com", password="12345"
        )
        self.user2 = User.objects.create_user(
            email="testuser2@gmail.com", password="1234"
        )
        self.task = Task.objects.create(
            title="test task",
            description="this is test task",
            assigned_to=self.user2,
            assigned_by=self.user,
            end_date="2024-12-24",
        )
        self.url = reverse("TaskView")

    def test_all_task_authenticated(self):
        self.client.login(email="testuser@gmail.com", password="12345")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test task")

    def test_all_task_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse("loginform"))
