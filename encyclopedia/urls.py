from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:name>', views.page, name="page"),
    path("results", views.results, name="search_results"),
    path("create", views.create_page, name="create"),
    path("edit", views.edit_page, name="edit"),
    path("random", views.random_entry, name="random"),
    path("wiki", views.wiki, name="redirect")
]
