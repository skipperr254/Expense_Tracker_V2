from django.contrib import admin
from .models import Expense, Category, Income

# Register your models here.
admin.site.register(Expense)
admin.site.register(Category)
admin.site.register(Income)