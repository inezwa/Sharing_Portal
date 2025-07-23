from django.urls import path
from . import views
from .api import material_search_api
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.material_list, name='material-list'),
    path('material/<int:pk>/', views.material_detail, name='material-detail'),
    path('upload/', views.upload_material, name='material-upload'),
    path('api/materials/', material_search_api, name='material-search-api'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),


]
