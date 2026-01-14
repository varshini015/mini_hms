from django.urls import path
from .views import (
    signup_view,
    login_view,
    logout_view,
    dashboard_view,
    doctor_dashboard,
    patient_dashboard,
    google_login,
    google_callback,
)

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('doctor/', doctor_dashboard, name='doctor_dashboard'),
    path('patient/', patient_dashboard, name='patient_dashboard'),

    path('google/login/', google_login, name='google_login'),
    path('google/callback/', google_callback, name='google_callback'),

]
