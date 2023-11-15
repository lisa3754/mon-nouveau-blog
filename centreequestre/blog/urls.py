from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('character/<str:id_character>/', views.post_detail, name='post_detail'),
    path('character/<str:id_character>/?<str:message>', views.post_detail, name='post_detail_mes'),
]