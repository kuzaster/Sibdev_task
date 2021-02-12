import csv
from collections import defaultdict
from datetime import datetime

from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Customer, Deals
from .serializers import CustomerSerializer, FileUploadSerializer

# Create your views here.


class CustomersView(APIView):
    parser_class = (FileUploadParser,)
    serializer_class = FileUploadSerializer

    def get(self, request):
        customers = Customer.objects.order_by("-spent_money")[:5]
        serialized_cust = CustomerSerializer(customers, many=True)
        filtered_deals = self.filter_deals(customers, serialized_cust)
        return Response({"response": filtered_deals.data})

    @staticmethod
    def filter_deals(customers, serialized_cust):
        count_gems = defaultdict(int)
        for ind, customer in enumerate(customers):
            gems = (
                Deals.objects.filter(customer=customer)
                .values_list("item", flat=True)
                .distinct()
            )
            serialized_cust.data[ind]["gems"] = list(gems)
            for gem in gems:
                count_gems[gem] += 1
        for cust in serialized_cust.data:
            cust["gems"] = list(filter(lambda key: count_gems[key] >= 2, cust["gems"]))
        return serialized_cust

    def post(self, request):
        file_obj = request.data["deals"]
        if not file_obj:
            raise ParseError("No file. Please upload file")
        if not file_obj.name.endswith(".csv"):
            raise ParseError(f"Invalid format of file. Should be .csv")

        csv_data = csv.DictReader(
            (line.decode("utf-8") for line in file_obj), delimiter=","
        )

        if Customer.objects.all().exists():
            Deals.objects.all().delete()
            Customer.objects.all().delete()
        for row in csv_data:
            username, gem, total, quantity, date = self.validate_data(row)
            try:
                customer = Customer.objects.get(username=username)
                customer.spent_money += total
            except Customer.DoesNotExist:
                customer = Customer.objects.create(username=username, spent_money=total)
            customer.save()
            Deals.objects.create(
                customer=customer, item=gem, cost=total, quantity=quantity, date=date
            )

        return Response(status=202, data="OK - файл был обработан без ошибок")

    @staticmethod
    def validate_data(row):
        if len(row.values()) != 5:
            raise ParseError("Data more than columns. Should be 5.")
        username, gem, total, quantity, date = row.values()
        if not (total.isnumeric() and quantity.isnumeric()):
            raise ParseError("Invalid format of total or quantity. Should be numeric.")
        try:
            datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            raise ParseError("Invalid format of date. Should be %Y-%m-%d %H:%M:%S.%f")
        return (
            username,
            gem,
            int(total),
            int(quantity),
            datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f"),
        )
