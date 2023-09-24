from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    bookId = models.PositiveIntegerField()
    title = models.CharField(max_length=100)
    authors = models.CharField(max_length=200)
    average_ratings = models.FloatField(blank=True, null=True)
    isbn = models.IntegerField()
    isbn13 = models.IntegerField(null=True)
    language = models.CharField(max_length=10)
    num_pages = models.PositiveIntegerField(blank=True, null=True)
    ratings_count = models.PositiveIntegerField(blank=True, null=True)
    text_reviews_count = models.IntegerField(blank=True, null=True)
    publication_date = models.DateField()
    publisher = models.CharField(max_length=200)
    price = models.IntegerField()

    class Meta:
        ordering = ['bookId']

    def __str__(self):
        return f'{self.title}'

class Members(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=20)
    image = models.FileField(upload_to="")

    def __str__(self):
        return f'{self.user.get_full_name()}'

class Transaction(models.Model):
    member_id = models.CharField(max_length=10)
    isbn =models.CharField(max_length=50)
    amount_paid = models.IntegerField()
    amount_remaining = models.IntegerField()
    issued_date = models.DateField(null=True)
    return_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-issued_date']