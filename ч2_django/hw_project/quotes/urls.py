from django.urls import path
from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main, name="main"),
    path("author/", views.author, name="author"),
    path("author/<str:slug_author>/", views.author_info, name="author_info"),
    path("quote/", views.quote, name="quote"),
]
