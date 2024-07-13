from django.urls import path
from .views import log_list, log_detail, chart_page, contact_sent

urlpatterns = [
    path("log_tracker/", log_list, name="log-list"),
    path("log_tracker/<int:id>/", log_detail, name="log-detail"),
    path("log_tracker/chart", chart_page, name="log-display"),
]
