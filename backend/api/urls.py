from django.urls import path

from api.views import AIChatView, ContentListView, HealthCheckView

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path("contents/", ContentListView.as_view(), name="content-list"),
    path("ai-chat/", AIChatView.as_view(), name="ai-chat"),
]