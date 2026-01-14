from .google_auth import get_google_flow
from google.oauth2.credentials import Credentials

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm

# SIGNUP (already working)
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


# LOGIN
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})

    return render(request, 'accounts/login.html')


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')


# DASHBOARD REDIRECT
@login_required
def dashboard_view(request):
    if request.user.role == 'doctor':
        return redirect('doctor_dashboard')
    elif request.user.role == 'patient':
        return redirect('patient_dashboard')

@login_required
def doctor_dashboard(request):
    if request.user.role != 'doctor':
        return redirect('dashboard')
    return render(request, 'accounts/doctor_dashboard.html')


@login_required
def patient_dashboard(request):
    if request.user.role != 'patient':
        return redirect('dashboard')
    return render(request, 'accounts/patient_dashboard.html')

@login_required
def google_login(request):
    flow = get_google_flow()
    auth_url, _ = flow.authorization_url(prompt='consent')
    return redirect(auth_url)


@login_required
def google_callback(request):
    flow = get_google_flow()
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    credentials = flow.credentials

    request.user.google_access_token = credentials.token
    request.user.google_refresh_token = credentials.refresh_token
    request.user.save()

    return redirect('dashboard')

