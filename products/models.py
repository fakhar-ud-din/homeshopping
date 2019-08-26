# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(verbose_name="Category Name", max_length=50)
    banner = models.ImageField(
        verbose_name="Category Banner", upload_to='banners/')

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(verbose_name="SubCategory Name", max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(verbose_name='Product Name', max_length=50)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    description = models.TextField(verbose_name='Product Description')
    short_description = models.TextField(
        verbose_name='Product Short Description', default='Description Available at Item Page')
    pictures = models.ImageField(
        verbose_name='Product Image', upload_to='products/')
    is_available = models.IntegerField(
        verbose_name='Availability', null=False, default=1)

    def __str__(self):
        return self.name


class WishList(models.Model):
    username = models.CharField(max_length=50)
    item_name = models.CharField(max_length=50)


class Cart(models.Model):
    username = models.CharField(max_length=50)
    item_name = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)


class Reviews(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    review = models.CharField(max_length=200)
    item = models.CharField(max_length=100)
    date = models.DateTimeField(verbose_name="Review Date")

    def __str__(self):
        return self.name


class Order(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=50, blank=False)
    address = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=50, blank=False)
    country = models.CharField(max_length=50, blank=False)
    zip_code = models.IntegerField(blank=False)
    phone = models.IntegerField(blank=False)

    def __str__(self):
        return self.email


class OrderBy(models.Model):
    order_id = models.IntegerField()
    ordered_by = models.ForeignKey(Order, on_delete=models.CASCADE, default="")
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_placed = models.DateField(
        verbose_name="Date of Order Placement", default="")
    payment_type = models.CharField(max_length=20, default="Bank Transfer")
