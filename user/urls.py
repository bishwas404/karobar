from django.urls import path
from user import views
from .views import login_view
urlpatterns = [
    path('login/',views.login_view ,name='login'),
    path('register/', views.register_page, name='register_page'),
    path('dashboard/', views.dashboard_page, name='dashboard_page'),
    path('transactions/', views.transactions_page, name='transactions_page'),
    path('api/create/',views.CreateUserView.as_view(),name='create'),
    path('api/login/',views.CreateTokenView.as_view(),name='api-login'),
    path('api/me/',views.ManageUserView.as_view(),name='me'),

]
