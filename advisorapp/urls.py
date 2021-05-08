from django.urls import path, include
from advisorapp import views
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('user/register/', views.CreateUserAccount.as_view()),
    path('token-refresh/', jwt_views.TokenRefreshView.as_view()),
]
