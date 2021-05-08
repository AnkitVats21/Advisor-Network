from django.urls import path, include
from advisorapp import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('user/register/', views.CreateUserAccount.as_view()),
    path('user/login/', views.UserLoginView.as_view()),
    path('user/login/', views.UserLoginView.as_view()),
    path('token-refresh/', jwt_views.TokenRefreshView.as_view()),
    path('admin/advisor/', views.AdvisorView.as_view()),
    path('user/<int:userid>/advisor/', views.AdvisorListView.as_view()),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)