from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry_title>", views.entry, name="entry"),
    path("<str:entry_title>/wiki:<str:wikioption>", views.wikioption, name="wikioption"),
    path("wiki:<str:wikipage>", views.wikipage, name="wikipage")

]
