from django.contrib import admin
from .models import *
# Register your models here.

# tạo csdl vào admin django
admin.site.register(Catagory)
admin.site.register(Product)
admin.site.register(Cart)

