from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

# Model representing expense categories.
class Category(models.Model):
    name = models.CharField(max_length=100)
    date_added = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=2)  # User associated with this category.
    is_global = models.BooleanField(default=True)  # True for global, False for user-specific

    def __str__(self):
        return self.name

# Model representing income records.
class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User associated with this income record.
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Income amount.
    date_added = models.DateField(default=timezone.now)  # Date when the income record was added.

# Model representing expense records.
class Expense(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User associated with this expense record.
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Category of the expense.
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Expense amount.
    date = models.DateField(default=timezone.now)  # Date of the expense.
    description = models.TextField(null=True)  # Description of the expense.

    def __str__(self):
        return self.name
