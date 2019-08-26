# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name')


@admin.register(models.OrderBy)
class OrderByAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'username', 'item',
                    'date_placed', 'payment_type')


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(models.SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description',
                    'category', 'subcategory', 'pictures', 'is_available')


@admin.register(models.WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ('username', 'item_name')


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('username', 'item_name')


@admin.register(models.Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'item')
