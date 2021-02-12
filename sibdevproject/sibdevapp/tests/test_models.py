from datetime import datetime

from django.test import TestCase

from ..models import Customer, Deals


class CustomerTest(TestCase):
    def setUp(self):
        Customer.objects.create(username="customer_1", spent_money=300)
        Customer.objects.create(username="customer_2", spent_money=500)

    def test_customer(self):
        customer_1 = Customer.objects.get(username="customer_1")
        customer_2 = Customer.objects.get(username="customer_2")

        self.assertEqual(customer_1.spent_money, 300)
        self.assertEqual(customer_2.spent_money, 500)


class DealsTest(TestCase):
    def setUp(self):
        self.date = datetime.strptime(
            "2018-12-14 08:29:45.883282", "%Y-%m-%d %H:%M:%S.%f"
        )
        self.customer_1 = Customer.objects.create(
            username="customer_1", spent_money=300
        )
        self.customer_2 = Customer.objects.create(
            username="customer_2", spent_money=500
        )
        Deals.objects.create(
            customer=self.customer_1, item="Кварц", cost=300, quantity=7, date=self.date
        )
        Deals.objects.create(
            customer=self.customer_2,
            item="Изумруд",
            cost=500,
            quantity=13,
            date=self.date,
        )

    def test_customer(self):
        deal_1 = Deals.objects.get(customer=self.customer_1)
        deal_2 = Deals.objects.get(customer=self.customer_2)

        self.assertEqual(
            str(deal_1),
            f"customer_1 bought 7 Кварц for 300RUB on {self.date.astimezone()}",
        )
        self.assertEqual(
            str(deal_2),
            f"customer_2 bought 13 Изумруд for 500RUB on {self.date.astimezone()}",
        )
