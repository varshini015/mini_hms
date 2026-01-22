from django.contrib import admin
from django.urls import path, include
from .views import serverless_test

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("serverless-test/", serverless_test),

]

