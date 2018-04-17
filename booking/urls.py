from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book),
    path('tick/', views.tick),
    path('reset/', views.reset),
]
