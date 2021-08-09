from django.urls import path
from rest_framework.routers import SimpleRouter

from users.views import UserAccountListViewset, AccountMonthlyReportAPIView


router = SimpleRouter()
router.register(r'accounts', UserAccountListViewset)


urlpatterns = [
    path(
        'accounts/<account_id>/monthly-report/<int:year>/<int:month>',
        AccountMonthlyReportAPIView.as_view(),
        name='monthly-report',
    ),
]
