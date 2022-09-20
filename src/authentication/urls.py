from django.urls import path

from authentication.api import views

urlpatterns = [
    path("auth/login/", views.LoginView.as_view(), name="token-obtain"),
    path("auth/refresh/", views.RefreshView.as_view(), name="token-refresh"),
    path("auth/logout/", views.LogOutView.as_view(), name="logout"),
    path("users/me/", views.UserDetailView.as_view(), name="user-detail"),
]
