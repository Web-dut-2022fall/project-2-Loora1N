from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE


class User(AbstractUser):
    pass


class Listing(models.Model):
    CATEGORY_CHOICES = [
        ('FS', 'Fashion'),
        ('TY', 'Toys'),
        ('ET', 'Electronics'),
        ('HM', 'Home')
    ]
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    startingBid = models.DecimalField(max_digits=8, decimal_places=2)
    currentPrice = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    image = models.ImageField(upload_to='static', blank=True)
    category = models.CharField(max_length=2, blank=True, choices=CATEGORY_CHOICES)
    listedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creater')
    winner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='winner')
    isActive = models.BooleanField()


class Biding(models.Model):
    bid = models.DecimalField(max_digits=8, decimal_places=2)
    bider = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)


class Comments(models.Model):
    comment = models.CharField(max_length=128)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)


class Watch(models.Model):
    watcher = models.OneToOneField(User, on_delete=models.CASCADE)
    list = models.ManyToManyField(Listing, blank=True)