from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('recommended/', views.recommended, name='recommended'),
    # mybox
    path('mybox/', views.mybox, name='mybox'),
    path('<int:movie_pk>/create_my_box/', views.create_my_box, name='create_my_box'),
    # video
    path('<int:movie_pk>/video/', views.video, name='video'),
    # pay
    path('pay/', views.pay, name='pay'),

]

