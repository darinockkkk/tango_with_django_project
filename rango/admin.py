from django.contrib import admin
from rango.models import Category, Page

#admin.ModelAdmins customizes how a model appears in the Django admin panel.
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url') 

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',) 

# Register models with custom admin views
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
