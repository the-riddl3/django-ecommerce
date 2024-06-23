# product urls
from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.show, name='show'),
]