from django.urls import path
from .views import (
    UserRegistrationView, UserLoginView, UserLogoutView, 
    GlobalCategoryListCreateView, GlobalCategoryRetrieveUpdateDestroyView, 
    UserCategoryListCreateView, UserCategoryRetrieveUpdateDestroyView,
    IncomeListCreateView, IncomeRetrieveUpdateDestroyView,
    ExpenseListCreateView, ExpenseRetrieveUpdateDestroyView,
    DashboardView, BlacklistTokenView, UserProfileView
)

urlpatterns = [
    # Other URL patterns
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path("logout/blacklist", BlacklistTokenView.as_view(), name="blacklist"),
    path('global-categories/', GlobalCategoryListCreateView.as_view(), name='global-category-list-create'),
    path('global-categories/<int:pk>/', GlobalCategoryRetrieveUpdateDestroyView.as_view(), name='global-category-retrieve-update-destroy'),
    path('user-categories/', UserCategoryListCreateView.as_view(), name='user-category-list-create'),
    path('user-categories/<int:pk>/', UserCategoryRetrieveUpdateDestroyView.as_view(), name='user-category-retrieve-update-destroy'),
    path('incomes/', IncomeListCreateView.as_view(), name='income-list-create'),
    path('incomes/<int:pk>/', IncomeRetrieveUpdateDestroyView.as_view(), name='income-retrieve-update-destroy'),
    path('expenses/', ExpenseListCreateView.as_view(), name='expense-list-create'),
    path('expenses/<int:pk>/', ExpenseRetrieveUpdateDestroyView.as_view(), name='expense-retrieve-update-destroy'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),

]