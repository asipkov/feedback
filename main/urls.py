from django.urls import path
from main import views
from .views import LoginView, RegistrationView
from django.contrib.auth import views as authViews
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', views.main, name='home'),
                  path('ratings/', views.Ratings.as_view(), name='ratings'),
                  path('login/', LoginView.as_view(), name='login'),
                  path('registration/', RegistrationView.as_view(), name='registration'),
                  path('exit/', authViews.LogoutView.as_view(next_page='/'), name='exit'),
                  path('id<int:user_id>/', views.profile, name='profile'),
                  path('edit/<int:id>/', views.edit, name='edit'),
                  path('my<int:user_id>/', views.my_profile, name='my_profile')

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
