from django.contrib import admin
from .models import Category, StudyMaterial

#custommizing how studymaterial appears in admin 
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'uploaded_by', 'upload_date')  # Columns shown in list view
    list_filter = ('category', 'upload_date')  # Adds filters on the right
    search_fields = ('title', 'description')  # Adds a search bar
    actions = ['approve_materials']

    def approve_materials(self, request, queryset):
        queryset.update(approved=True)
    approve_materials.short_description = "Approve selected materials"

# Register models to appear in admin panel
admin.site.register(Category)
admin.site.register(StudyMaterial, StudyMaterialAdmin)


