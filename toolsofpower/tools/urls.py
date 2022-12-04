from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),    
    path('parser/', views.parser, name='parser'),
    path('tool/<uuid:tool>', views.tool, name='tool'),
]
