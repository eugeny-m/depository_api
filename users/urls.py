from django.urls import path
from users.views import UserAccountMonthlyReport


urlpatterns = [
    path(
        'accounts/<account_id>/monthly-report/<int:year>/<int:month>',
        UserAccountMonthlyReport.as_view(),
        name='monthly-report',
    ),
]
