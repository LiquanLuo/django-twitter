from testing.testcases import TestCase
from rest_framework.test import APIClient

LOGIN_URL = '/api/accounts/login/'
LOGOUT_URL = '/api/accounts/logout/'
SIGNUP_URL = '/api/accounts/signup/'
LOGIN_STATUS_URL = '/api/accounts/login_status/'

class AccountAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = self.create_user(
            username='abcdefg',
            email='admin@gg.com',
            password='correct'
        )

    def test_login(self):
        # test GET, return 405 = METHOD_NOT_ALLOWED
        response = self.client.get(LOGIN_URL,{
            "username":self.user.username,
            "password":self.user.password,
        })
        self.assertEqual(response.status_code, 405)

        # test wrong password, 400 = Bad Request response
        response = self.client.post(LOGIN_URL, {
            "username": self.user.username,
            "password": 'wrong password',
        })
        # print(response.data)
        self.assertEqual(response.status_code, 400)

        # test login status = false
        response = self.client.get(LOGIN_STATUS_URL)
        # print(response.data)
        self.assertEqual(response.data['login'], False)

        # test login successfully
        response = self.client.post(LOGIN_URL, {
            "username": self.user.username,
            "password": 'correct',
        })
        # print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['user'], None)
        self.assertEqual(response.data['user']['email'], 'admin@gg.com')

        # test login status =  true
        response = self.client.get(LOGIN_STATUS_URL)
        # print(response.data)
        self.assertEqual(response.data['login'], True)

    def test_logout(self):
        # print("-----------logout test start ------------")
        # login
        self.client.post(LOGIN_URL, {
            "username": self.user.username,
            "password": "correct",
        })

        # login status, True
        response = self.client.get(LOGIN_STATUS_URL)
        # print(response.data)
        self.assertEqual(response.data['login'], True)

        # test get method, return 405 = METHOD_NOT_ALLOWED
        response = self.client.get(LOGOUT_URL)
        # print(response.data)
        self.assertEqual(response.status_code, 405)

        # logout successfully return 200
        response = self.client.post(LOGOUT_URL)
        # print(response.data)
        self.assertEqual(response.status_code, 200)

        # test login status, False
        response = self.client.get(LOGIN_STATUS_URL)
        # print(response.data)
        self.assertEqual(response.data['login'], False)

        # print("-----------logout test end ------------")


    def test_signup(self):
        # print("-----------signup test start ------------")

        data = {
            'username': 'someone1',
            'email': 'someone@gg.com',
            'password': 'any password',
        }

        # test get method failed, return 405 = METHOD_NOT_ALLOWED
        response = self.client.get(SIGNUP_URL, data)
        # print(response.data)
        self.assertEqual(response.status_code, 405)

        # test wrong format email
        response = self.client.post(SIGNUP_URL, {
            'username': 'someone',
            'email': 'wrong email',
            'password': 'any password'
        })
        # print(response.data)
        self.assertEqual(response.status_code, 400)

        # test too short password
        response = self.client.post(SIGNUP_URL, {
            'username': 'someone',
            'email': 'wrong email',
            'password': 'a'
        })
        # print(response.data)
        self.assertEqual(response.status_code, 400)

        # test too long username
        response = self.client.post(SIGNUP_URL, {
            'username': '012345678901234567890123456',
            'email': 'wrong email',
            'password': 'a'
        })
        # print(response.data)
        self.assertEqual(response.status_code, 400)

        # test signup successfully
        response = self.client.post(SIGNUP_URL, data)
        # print(response.data)
        self.assertEqual(response.status_code, 200)

        # test login status
        response = self.client.get(LOGIN_STATUS_URL)
        # print(response.data)
        self.assertEqual(response.data['login'], True)

        # print("-----------signup test end --------------")











