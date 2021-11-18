from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('recommended/', views.recommended, name='recommended'),
    # mybox
    path('mybox/', views.mybox, name='mybox'),
    #path('mybox_add/', views.mybox, name='mybox'),
    #path('mybox/', views.mybox, name='mybox'),



]
