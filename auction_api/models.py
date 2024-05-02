from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    min_bid = models.IntegerField()
    start_time = models.DateTimeField(default=timezone.now)
    last_bid_time = models.DateTimeField(default=timezone.now)
    current_highest_bid = models.IntegerField(default=0)
    current_highest_bidder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name



class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bids')
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - ${self.amount}"

    @staticmethod
    def place_bid(user, product, amount):

        if amount < product.min_bid:
            raise ValueError("Bid amount must be greater than or equal to the minimum bid.")

        if amount > product.current_highest_bid:
            product.current_highest_bid = amount
            product.current_highest_bidder = user
            product.save()

        # Create the bid object
        bid = Bid.objects.create(user=user, product=product, amount=amount)
        return bid

