from . import views
from django.urls import include, path


urlpatterns = [
    path('signin/', views.SignIn.as_view(), name="signin"),
    path('signup/', views.SignUp.as_view(), name="signup"),
]
