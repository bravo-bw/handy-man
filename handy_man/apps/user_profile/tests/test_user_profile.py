import os
from django.conf import settings
from django.test import TestCase

from .factories import UserProfileFactory


class TestUserProfile(TestCase):

    def setUp(self):
        pass

    def test_document(self):
        user_profile = UserProfileFactory()
        self.assertEqual(user_profile.document(user_profile.document_1), '')
        test_file = open('test_file.txt', 'w+')
        test_file.write('test_file\n')
        test_file.close()
        user_profile.document_1 = test_file
        self.assertEqual(user_profile.document(user_profile.document_1), '{}gfx/{}'.format(settings.STATIC_URL, 'test_file.txt'))
        os.remove('test_file.txt')

    def test_document_urls(self):
        user_profile = UserProfileFactory()
        test_file = open('test_file.txt', 'w+')
        test_file.write('test_file\n')
        test_file.close()
        user_profile.document_1 = test_file
        user_profile.document_2 = test_file
        user_profile.document_3 = test_file
        self.assertEqual(len(user_profile.document_urls), 3)
        os.remove('test_file.txt')

    def test_avatar_name(self):
        user_profile = UserProfileFactory()
        print(user_profile.avatar_name)
        self.assertEqual(user_profile.avatar_name, '{}gfx/{}'.format(settings.STATIC_URL, 'default_avatar_male.jpg'))
        test_file = open('test_file.jpg', 'w+')
        test_file.write('test_file\n')
        test_file.close()
        user_profile.avatar_image = test_file
        self.assertEqual(user_profile.avatar_name, '{}gfx/{}'.format(settings.STATIC_URL, 'test_file.jpg'))
        os.remove('test_file.jpg')
