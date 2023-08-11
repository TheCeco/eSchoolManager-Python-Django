from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase, Client
from django.urls import reverse

from eSchoolManager.classes_app.models import ClassesModel, TeacherClass
from eSchoolManager.common_app.models import SubjectsModel
from eSchoolManager.principal_app.models import TeacherSubjects
from eSchoolManager.teachers_app.models import TeacherProfile

UserModel = get_user_model()


class TeacherDetailsViewTest(TestCase):
    VALID_TEACHER_USER_DATA = {
        'email': 'teacher@abv.bg',
        'first_name': 'Teacher',
        'last_name': 'Teacher',
        'password': 'testpassword'
    }

    VALID_TEACHER_PROFILE_DATA = {
        'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRb7b5Uk6-fslFsGiTi_zqcNqdn9QqIC8AMxw&usqp=CAU',
        'gender': 'male',
        'date_of_birth': '2001-09-09',
        'phone': '0897812215',
        'address': 'ul. Car Boris 1'
    }

    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(
            **self.VALID_TEACHER_USER_DATA
        )

        self.teacher = TeacherProfile.objects.create(
            **self.VALID_TEACHER_PROFILE_DATA,
            user=self.user
        )

        self._give_permissions(self.user, 'view_teacherprofile', 'view_schooluser')

        self._create_subject('Maths', 'Computer Science')
        self.teacher_classes = self._create_class_to_teacher(self.teacher, SubjectsModel.objects.get(subject_name='Maths'), '12', '11')
        self.teacher_subjects = self._create_subject_to_teacher(self.teacher, SubjectsModel.objects.all())

    def _create_class_to_teacher(self, teacher, subject, *classes):
        for clas in classes:
            self.clas = ClassesModel.objects.create(classes_choice=clas)
            TeacherClass.objects.create(teacher=teacher, school_class=self.clas, subject=subject)

        return TeacherClass.objects.filter(teacher=teacher)

    def _create_subject_to_teacher(self, teacher, subjects):
        for subject in subjects:
            TeacherSubjects.objects.create(teacher=teacher, subject=subject)

        return TeacherSubjects.objects.filter(teacher=teacher)

    def _create_subject(self, *subjects):
        for subject in subjects:
            SubjectsModel.objects.create(subject_name=subject)

    def _give_permissions(self, user, *permissions):
        for permission in permissions:
            teacher_permission = Permission.objects.get(codename=permission)
            user.user_permissions.add(teacher_permission)

    def test_get__with_authenticated_user__expect_to_return_200(self):
        self.client.force_login(self.user)
        url = reverse('teacher_details', kwargs={'pk': self.teacher.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teachers_templates/teacher_details.html')

    def test_get__when_try_to_go_to_other_user_details__expect_return_to_yours_details(
            self):
        other_data = {
            'email': 'other_teacher@example.com',
            'first_name': 'OtherTeacher',
            'last_name': 'OtherTeacher',
            'password': 'testpassword'
        }

        other_user = UserModel.objects.create_user(**other_data)

        self._give_permissions(other_user, 'view_teacherprofile', 'view_schooluser')

        other_teacher = TeacherProfile.objects.create(user=other_user)
        self.client.force_login(self.user)
        url = reverse('teacher_details', kwargs={'pk': other_teacher.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.teacher.user.get_full_name())

    def test_get__with_unauthenticated_user__expect_to_redirect_to_login_view(self):
        url = reverse('teacher_details', kwargs={'pk': self.teacher.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/profile/login/?next=' + url)

    def test_get__with_non_authorised_user__expect_to_return_403(self):
        other_data = {
            'email': 'other_teacher@example.com',
            'first_name': 'OtherTeacher',
            'last_name': 'OtherTeacher',
            'password': 'testpassword'
        }

        other_user = UserModel.objects.create_user(**other_data)
        self.client.force_login(other_user)

        url = reverse('teacher_details', kwargs={'pk': self.teacher.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_get__with_non_existed_teacher__expect_to_return_500(self):
        other_data = {
            'email': 'other_teacher@example.com',
            'first_name': 'OtherTeacher',
            'last_name': 'OtherTeacher',
            'password': 'testpassword'
        }

        other_user = UserModel.objects.create_user(**other_data)
        self._give_permissions(other_user, 'view_teacherprofile', 'view_schooluser')
        self.client.force_login(other_user)

        url = reverse('teacher_details', kwargs={'pk': 2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_get__profile_details__expect_to_display_details(self):
        self.client.force_login(self.user)
        url = reverse('teacher_details', kwargs={'pk': self.teacher.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.teacher.user.get_full_name())

    def test_get__subjects__expect_to_displayed_teacher_subjects(self):
        self.client.force_login(self.user)
        url = reverse('teacher_details', kwargs={'pk': self.teacher.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for teacher_subject in self.teacher_subjects:
            self.assertContains(response, teacher_subject.subject)

    def test_displayed_classes(self):
        self.client.force_login(self.user)
        url = reverse('teacher_details', kwargs={'pk': self.teacher.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for teacher_class in self.teacher_classes:
            self.assertContains(response, teacher_class.school_class)
