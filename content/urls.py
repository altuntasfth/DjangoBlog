from django.urls import path, include

from content import views

urlpatterns = [
    path('', views.index, name='index'),

]
