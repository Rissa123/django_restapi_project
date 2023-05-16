from django.urls import path
from .views import LoginView,OverviewAPI, CreateAPI, DetailAPI, UpdateAPI, DeleteAPI
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('overview/', OverviewAPI.as_view(), name='snippet-overview'),
    path('create/', CreateAPI.as_view(), name='snippet-create'),
    path('detail/<int:pk>/', DetailAPI.as_view(), name='snippet-detail'),
    path('update/<int:pk>/', UpdateAPI.as_view(), name='snippet-update'),
    path('delete/<int:pk>/', DeleteAPI.as_view(), name='snippet-delete'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

