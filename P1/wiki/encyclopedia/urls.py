from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.page, name="wikipage"),
    path("search/", views.search, name="search"),
    path("newpage/", views.new_page, name="newpage"),
    path("edit/<str:title>", views.edit_page, name="edit")
]
