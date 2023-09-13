from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .serializers import (
    UserRegistrationSerializer, GlobalCategorySerializer, UserCategorySerializer, 
    IncomeSerializer, ExpenseSerializer, DashboardSummarySerializer, UserProfileSerializer
    )
from .models import Category, Income, Expense
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
class UserRegistrationView(generics.CreateAPIView):
    """
    View for user registration.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

class UserLoginView(APIView):
    """
    View for user login.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Authenticate user and generate a token upon successful login.
        """
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutView(APIView):
    """
    View for user logout.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Invalidate the user's authentication token upon logout.
        """
        request.auth.delete()  # Invalidate the user's authentication token
        logout(request)
        return Response({'detail': 'Logged out successfully'}, status=status.HTTP_200_OK)

class BlacklistTokenView(APIView):
    """
    View to blacklist JWT tokens.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Blacklist a JWT token.
        """
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class GlobalCategoryListCreateView(generics.ListCreateAPIView):
    """
    View for listing and creating global categories.
    """
    queryset = Category.objects.filter(is_global=True)
    serializer_class = GlobalCategorySerializer
    permission_classes = [IsAdminOrReadOnly]  # You can adjust permissions as needed

class GlobalCategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting global categories.
    """
    queryset = Category.objects.filter(is_global=True)
    serializer_class = GlobalCategorySerializer
    permission_classes = [IsAdminOrReadOnly]  # You can adjust permissions as needed

class UserCategoryListCreateView(generics.ListCreateAPIView):
    """
    View for listing and creating user-specific categories.
    """
    serializer_class = UserCategorySerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user, is_global=False)

class UserCategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting user-specific categories.
    """
    serializer_class = UserCategorySerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user, is_global=False)

class IncomeListCreateView(generics.ListCreateAPIView):
    """
    View for listing and creating income records.
    """
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

class IncomeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting income records.
    """
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

class ExpenseListCreateView(generics.ListCreateAPIView):
    """
    View for listing and creating expense records.
    """
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

class ExpenseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting expense records.
    """
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

class DashboardView(generics.RetrieveAPIView):
    """
    View for generating a dashboard summary.
    """
    serializer_class = DashboardSummarySerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user = self.request.user

        # Calculate total income
        total_income = Income.objects.filter(user=user).aggregate(total_income=models.Sum('amount'))['total_income'] or 0.0

        # Calculate total expenses
        total_expenses = Expense.objects.filter(user=user).aggregate(total_expenses=models.Sum('amount'))['total_expenses'] or 0.0

        # Calculate remaining income
        remaining_income = total_income - total_expenses

        # Calculate expense breakdown by category
        categories = Category.objects.all()
        expense_breakdown = {}
        for category in categories:
            expenses = Expense.objects.filter(user=user, category=category)
            total_category_expenses = expenses.aggregate(total_category_expenses=models.Sum('amount'))['total_category_expenses'] or 0.0
            expense_breakdown[category.name] = total_category_expenses

        summary_data = {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'remaining_income': remaining_income,
            'expense_breakdown': expense_breakdown,
        }

        return Response(summary_data)

class UserProfileView(APIView):
    """
    View for fetching the profile of the currently logged-in user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
