from django.urls import path
from . import views
# from .api import material_api

urlpatterns = [
    path('', views.material_list, name='material-list'),  # Homepage (list all materials)
    path('<int:pk>/', views.material_detail, name='material-detail'),  # Single material view
    path('upload/', views.upload_material, name='material-upload'),
    path('upload/', views.upload_material, name='material-upload'),
    # path('api/materials/', material_api, name='material-api'),
]
