from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from ads import views

urlpatterns = [
    path('', views.AdUserListView.as_view()),
    path('<int:pk>/', views.AdUserDetailView.as_view()),
    path('create/', views.AdUserCreateView.as_view()),
    path('<int:pk>/update/', views.AdUserUpdateView.as_view()),
    path('<int:pk>/delete/', views.AdUserDeleteView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]

