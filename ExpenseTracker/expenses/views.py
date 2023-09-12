from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer, GlobalCategorySerializer, UserCategorySerializer, IncomeSerializer, ExpenseSerializer, DashboardSummarySerializer
from .models import Category, Income, Expense
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()  # Invalidate the user's authentication token
        logout(request)
        return Response({'detail': 'Logged out successfully'}, status=status.HTTP_200_OK)
    


class BlacklistTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    

class GlobalCategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.filter(is_global=True)
    serializer_class = GlobalCategorySerializer
    permission_classes = [IsAdminOrReadOnly]  # You can adjust permissions as needed

class GlobalCategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.filter(is_global=True)
    serializer_class = GlobalCategorySerializer
    permission_classes = [IsAdminOrReadOnly]  # You can adjust permissions as needed

class UserCategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = UserCategorySerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user, is_global=False)

class UserCategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserCategorySerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user, is_global=False)
    


class IncomeListCreateView(generics.ListCreateAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)
    

class IncomeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)
    


class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

class ExpenseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)
    



class DashboardView(generics.RetrieveAPIView):
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