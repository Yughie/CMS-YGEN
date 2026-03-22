from django.urls import path

from api.views import ContentListView, HealthCheckView

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path("contents/", ContentListView.as_view(), name="content-list"),
]