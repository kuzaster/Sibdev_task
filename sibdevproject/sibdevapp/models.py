from django.db import models

# Create your models here.


class Customer(models.Model):
    username = models.CharField(max_length=30, primary_key=True)
    spent_money = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.username}"


class Deals(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.CharField(max_length=30)
    cost = models.IntegerField()
    quantity = models.IntegerField()
    date = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.customer} bought {self.quantity} {self.item} for {self.cost}RUB on {self.date}"
