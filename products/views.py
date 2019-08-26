# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Product, Category, SubCategory, Reviews, Cart, WishList
from django import forms
from django.views.generic import TemplateView
from datetime import datetime

# Create your views here.


class ReviewForm(forms.Form):
    name = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Your Name', 'style': 'margin-left:20px'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'input', 'placeholder': 'Your Email', 'style': 'margin-left:20px'}))
    review = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'input', 'placeholder': 'Say something about the Product!', 'style': 'width:350px;margin-left:20px;'}))


class CategoryClass(TemplateView):
    products = Product.objects.all()

    def get(self, request, *args, **kwargs):
        arguments_returned = get_cart_wishlist(request)
        title = kwargs['name']
        id_category = Category.objects.get(name=title)
        banner = Category.objects.get(name=title)
        subcategories = SubCategory.objects.filter(category=id_category)
        items = Product.objects.filter(category=id_category)
        categories = []
        for product in self.products:
            categories.append(product.category)
        categories = list(set(categories))
        categories.sort(key=lambda x: x.name.lower())
        subcategories = list(set(subcategories))
        subcategories.sort(key=lambda x: x.name.lower())
        arguments = {'title': title, 'items': items, 'products': self.products,
                     'subcategories': subcategories, 'categories': categories, 'banner': banner}
        arguments.update(arguments_returned)
        return render(request, "products/index.html", arguments)


class ItemClass(TemplateView):

    def get(self, request, *args, **kwargs):
        arguments_returned = get_cart_wishlist(request)
        title = kwargs['name']
        product = Product.objects.get(name=title)
        product_category = Category.objects.get(name=product.category)
        categories = Category.objects.all()
        products = Product.objects.filter(category=product_category)
        reviews = Reviews.objects.filter(item=title)
        count_reviews = len(reviews)

        categories = list(set(categories))
        categories.sort(key=lambda x: x.name.lower())

        submitted = False
        if request.method == "POST":
            form = ReviewForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                review_date = datetime.today()
                cd['item'] = name
                cd['date'] = review_date

                new_review = Reviews()
                new_review.name = cd['name']
                new_review.email = cd['email']
                new_review.review = cd['review']
                new_review.item = cd['item']
                new_review.date = cd['date']
                new_review.save()
                return HttpResponseRedirect('?submitted=True')
        else:
            form = ReviewForm()
            if 'submitted' in request.GET:
                submitted = True
        arguments = {'title': title, 'product': product, 'reviews': reviews, 'count_reviews': count_reviews,
                     'relevent_products': products, 'categories': categories, 'form': form, 'submitted': submitted}
        arguments.update(arguments_returned)
        return render(request, "products/item.html", arguments)


class BrandsClass(TemplateView):

    def get(self, request, *args, **kwargs):
        arguments_returned = get_cart_wishlist(request)
        title = kwargs['name']
        products = Product.objects.all()
        id_subcategory = SubCategory.objects.get(name=title)
        items = Product.objects.filter(subcategory=id_subcategory)
        subcategories = []
        categories = []
        for product in products:
            subcategories.append(product.subcategory)
            categories.append(product.category)
        subcategories = list(set(subcategories))
        categories = list(set(categories))
        subcategories.sort(key=lambda x: x.name.lower())
        categories.sort(key=lambda x: x.name.lower())
        arguments = {'title': title, 'items': items, 'products': products,
                     'subcategories': subcategories, 'categories': categories}
        arguments.update(arguments_returned)
        return render(request, "products/brands.html", arguments)


def get_cart_wishlist(request):
    username = request.user
    cart_count = 0
    wishlist_count = 0
    arguments = {'cart_count': cart_count, 'wishlist_count': wishlist_count}

    items_in_cart = Cart.objects.filter(username=username)
    items_in_wishlist = WishList.objects.filter(username=username)
    cart_items = []
    wishlist_items = []
    subtotal_cart = 0
    for item in items_in_cart:
        cart_items.append(Product.objects.get(name=item.item_name))
        subtotal_cart += ((Product.objects.get(name=item.item_name)
                           ).price * item.quantity)
    for item in items_in_wishlist:
        wishlist_items.append(Product.objects.get(name=item.item_name))

    cart_count = len(cart_items)
    wishlist_count = len(wishlist_items)
    arguments['cart_count'] = cart_count
    arguments['wishlist_count'] = wishlist_count
    arguments['cart_items'] = cart_items
    arguments['items_in_cart'] = items_in_cart
    arguments['wishlist_items'] = wishlist_items
    arguments['subtotal_cart'] = subtotal_cart
    return arguments
