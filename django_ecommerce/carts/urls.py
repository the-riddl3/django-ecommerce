

from django.urls import path

from carts import views

app_name = 'carts'
urlpatterns = [
    path('cart/', views.index, name='index'),
    path('update/', views.update, name='update'),
    path('delete/', views.delete, name='delete'),
]
