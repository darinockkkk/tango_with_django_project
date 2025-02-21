from django.contrib import admin
from rango.models import Category, Page

#adding classes to include them to the admin interface
admin.site.register(Category)
admin.site.register(Page)
