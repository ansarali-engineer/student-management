from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from students.views import StudentViewSet

router = DefaultRouter()
router.register("students", StudentViewSet, basename="student")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
