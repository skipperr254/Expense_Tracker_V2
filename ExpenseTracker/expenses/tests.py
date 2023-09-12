from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Category, Income, Expense
from .serializers import GlobalCategorySerializer

# Create your tests here.

class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.registration_url = reverse('user-registration')
        self.valid_user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
        }

    def test_user_registration(self):
        response = self.client.post(self.registration_url, self.valid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_user_registration_with_existing_username(self):
        User.objects.create_user(**self.valid_user_data)  # Create a user with the same username
        response = self.client.post(self.registration_url, self.valid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Add more registration test cases as needed

class UserLoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('user-login')
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_login(self):
        response = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_login_with_invalid_credentials(self):
        invalid_data = {'username': 'invaliduser', 'password': 'invalidpassword'}
        response = self.client.post(self.login_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Add more login test cases as needed

class UserLogoutTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.logout_url = reverse('user-logout')
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        self.user = User.objects.create_user(**self.user_data)
        # self.token = Token.objects.create(user=self.user)
        self.token, self.created = Token.objects.get_or_create(user=self.user)


    def test_user_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(self.logout_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(key=self.token.key).exists())

    def test_user_logout_without_authentication(self):
        response = self.client.post(self.logout_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Add more logout test cases as needed


class GlobalCategoryTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.global_categories_url = reverse('global-category-list-create')
        self.user = User.objects.create_user(username='testuser', password='testpassword', is_staff=True)
        self.global_category_data = {'name': 'Global Category 1', 'is_global': True, 'user_id': 1}
        self.token, _ = Token.objects.get_or_create(user=self.user)

    def test_list_global_categories(self):
        # Create a global category
        Category.objects.create(name='Global Category 1', is_global=True)
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(self.global_categories_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_global_category(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(self.global_categories_url, self.global_category_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Add more test cases for updating and deleting global categories as needed


class UserCategoryTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_categories_url = reverse('user-category-list-create')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_category_data = {'name': 'User Category 1', 'is_global': False, 'user': self.user}
        self.token, _ = Token.objects.get_or_create(user=self.user)

    def test_list_user_categories(self):
        # Create a user-specific category
        Category.objects.create(name='User Category 1', is_global=False, user=self.user)
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(self.user_categories_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_user_category(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(self.user_categories_url, self.user_category_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Add more test cases for updating and deleting user-specific categories as needed

class IncomeTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.incomes_url = reverse('income-list-create')
        self.income_data = {'amount': 1000.0, 'source': 'Salary'}
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token, _ = Token.objects.get_or_create(user=self.user)

    def test_list_incomes(self):
        # Create an income record for the user
        Income.objects.create(user=self.user, amount=1000.0, source='Salary')
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(self.incomes_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_income(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(self.incomes_url, self.income_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Add more test cases for updating and deleting income records as needed


class ExpenseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.expenses_url = reverse('expense-list-create')
        self.expense_data = {'amount': 100.0, 'description': 'Groceries'}
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token, _ = Token.objects.get_or_create(user=self.user)

    def test_list_expenses(self):
        # Create an expense record for the user
        Expense.objects.create(user=self.user, amount=100.0, description='Groceries')
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(self.expenses_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_expense(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(self.expenses_url, self.expense_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Add more test cases for updating and deleting expenses as needed



class DashboardTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.dashboard_url = reverse('dashboard')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token, _ = Token.objects.get_or_create(user=self.user)

    def test_dashboard_summary(self):
        # Create sample income records and expenses for the user
        Income.objects.create(user=self.user, amount=1000.0, source='Salary')
        Expense.objects.create(user=self.user, amount=200.0, description='Groceries')
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(self.dashboard_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_summary = {
            'total_income': 1000.0,
            'total_expenses': 200.0,
            'remaining_income': 800.0,
            'expense_breakdown': {},
        }

        self.assertEqual(response.data, expected_summary)

    # Add more test cases for various dashboard scenarios