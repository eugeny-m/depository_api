from django.utils import timezone

from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from operations.models import Operation
from users.models import Account
from users.serializers import AccountSerializer


class AccountMonthlyReportAPIView(APIView):

    def validate_path_params(self, year, month):
        now = timezone.now()
        if not 1 <= month <= 12:
            raise ValidationError(f'"{month}" is not a valid month number')
        if year > now.year:
            raise ValidationError(f'"{year}" is not a valid year number')
    
    def get(self, request, account_id, year, month):
        try:
            Account.objects.get(id=account_id)
        except Account.DoesNotExist:
            raise NotFound()
        self.validate_path_params(year, month)

        data = Operation.objects.filter(
            created__month=month,
            created__year=year,
            account_id=account_id,
        ).report()
        return Response(data)


class UserAccountListViewset(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
