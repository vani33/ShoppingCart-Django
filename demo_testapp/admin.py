from django.contrib import admin
from .models import Search, Category, Product
from django.contrib.auth import get_user_model
# Register your models here.

EasyCart = get_user_model()

class EasyCartAdmin(admin.ModelAdmin): #To  search by email field
    search_fields = ['email']
    class Meta:
        model = EasyCart

admin.site.register(EasyCart,EasyCartAdmin)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Search)
