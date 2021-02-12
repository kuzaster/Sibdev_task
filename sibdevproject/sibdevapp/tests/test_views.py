from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from ..models import Customer, Deals
from ..serializers import CustomerSerializer
from ..views import CustomersView

client = Client()


class FilterDealsByGemsTest(TestCase):
    fixtures = ["records_with_unique_gems.json"]

    def test_filter_deal(self):

        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)

        customer_1_gems = (
            Deals.objects.filter(customer="customer_1")
            .values_list("item", flat=True)
            .distinct()
        )
        customer_2_gems = (
            Deals.objects.filter(customer="customer_2")
            .values_list("item", flat=True)
            .distinct()
        )

        self.assertEqual(customers.count(), 2)
        self.assertIn("Яшма", customer_1_gems)
        self.assertNotIn("Яшма", customer_2_gems)

        filtered_deals = CustomersView.filter_deals(customers, serializer)
        customer_1 = filtered_deals.data[0]

        self.assertEqual(customer_1["username"], "customer_1")
        self.assertNotIn("Яшма", customer_1["gems"])


class GetTopFiveCustomerTest(TestCase):
    fixtures = ["first_db_records.json"]

    def test_get_top_five_customer(self):
        response = client.get(reverse("get_post_deals"))

        customers = Customer.objects.order_by("-spent_money")[:5]
        serializer = CustomerSerializer(customers, many=True)
        filtered_deals = CustomersView.filter_deals(customers, serializer)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["response"], filtered_deals.data)


class PostDealsFileTest(TestCase):
    def test_post_correct_deals_file(self):
        data = bytes(
            "customer,item,total,quantity,date\ncustomer,Изумруд,3136,8,2018-12-16 03:35:54.925057",
            "utf8",
        )
        csv_file = SimpleUploadedFile("deals.csv", data)

        self.assertFalse(Customer.objects.all().exists())
        self.assertFalse(Deals.objects.all().exists())

        response = client.post(reverse("get_post_deals"), data={"deals": csv_file})

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertTrue(Customer.objects.all().exists())
        self.assertTrue(Deals.objects.all().exists())
        self.assertEqual(Customer.objects.first().username, "customer")
        self.assertEqual(Deals.objects.first().item, "Изумруд")

    def test_post_deals_file_with_incorrect_file_extension(self):
        data = bytes(
            "customer,item,total,quantity,date\ncustomer,Изумруд,3136,8,2018-12-16 03:35:54.925057",
            "utf8",
        )
        csv_file = SimpleUploadedFile("deals.docs", data)

        response = client.post(reverse("get_post_deals"), data={"deals": csv_file})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["detail"], "Invalid format of file. Should be .csv"
        )


class ValidateDataTest(TestCase):
    def test_post_with_incorrect_quntity_of_rows(self):
        data = bytes(
            "customer,item,total,quantity,date\ncust,Опал,31,8,2018-12-16 03:35:54.925057,sixth",
            "utf8",
        )
        csv_file = SimpleUploadedFile("deals.csv", data)

        response = client.post(reverse("get_post_deals"), data={"deals": csv_file})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["detail"], "Data more than columns. Should be 5."
        )

    def test_post_with_incorrect_format_of_cost(self):
        data = bytes(
            "customer,item,total,quantity,date\ncust,Опал,STRING,8,2018-12-16 03:35:54.925057",
            "utf8",
        )
        csv_file = SimpleUploadedFile("deals.csv", data)

        response = client.post(reverse("get_post_deals"), data={"deals": csv_file})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["detail"],
            "Invalid format of total or quantity. Should be numeric.",
        )

    def test_post_with_incorrect_format_of_quantity(self):
        data = bytes(
            "customer,item,total,quantity,date\ncust,Опал,350,STRING,2018-12-16 03:35:54.925057",
            "utf8",
        )
        csv_file = SimpleUploadedFile("deals.csv", data)

        response = client.post(reverse("get_post_deals"), data={"deals": csv_file})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["detail"],
            "Invalid format of total or quantity. Should be numeric.",
        )

    def test_post_with_incorrect_format_of_date(self):
        data = bytes(
            "customer,item,total,quantity,date\ncust,Опал,350,6,2018-12-16", "utf8"
        )
        csv_file = SimpleUploadedFile("deals.csv", data)

        response = client.post(reverse("get_post_deals"), data={"deals": csv_file})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["detail"],
            "Invalid format of date. Should be %Y-%m-%d %H:%M:%S.%f",
        )
