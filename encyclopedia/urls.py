from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:page>", views.showPage, name="showPage"),
    path("create", views.create, name="create"),
    path("random", views.randomPage, name="random"),
    path("wiki/<str:page>/update", views.update, name="update")
    

]
