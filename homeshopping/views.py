from django.shortcuts import render
from products.models import Product, WishList, Cart, Order, OrderBy
from django.views.generic import TemplateView, ListView
from django.http import HttpResponseRedirect, HttpRequest
from django.contrib.auth.models import User
from datetime import date
from django.core.mail import send_mail, EmailMessage
from django.conf import settings


class Search(TemplateView):

    template_name = 'search-results.html'

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        products_uppercase = {}
        for product in products:
            products_uppercase[str(product.id)] = product.name.upper()

        query = request.GET.get('search-field')
        query = query.upper()

        found_products = []
        for ids in products_uppercase:
            if query in products_uppercase[ids]:
                found_products.append(
                    [x for x in products if str(x.id) == ids])
        refine_product_list = []
        for product in found_products:
            refine_product_list.append(product[0])

        return render(request, self.template_name, {'products': refine_product_list, })


class Checkout(TemplateView):
    template_name = 'checkout.html'

    username = None
    products = Product.objects.all()
    categories = []
    subcategories = []
    for product in products:
        categories.append(product.category)
        subcategories.append(product.subcategory)
    categories = list(set(categories))
    categories.sort(key=lambda x: x.name.lower())
    subcategories = list(set(subcategories))
    subcategories.sort(key=lambda x: x.name.lower())
    cart_count = 0
    wishlist_count = 0

    arguments = {'products': products,
                 'categories': categories, 'subcategories': subcategories, 'cart_count': cart_count, 'wishlist_count': wishlist_count}

    def get(self, request, *args, **kwargs):
        self.username = request.user
        if self.username != 'AnonymousUser':
            items_in_cart = Cart.objects.filter(
                username=self.username)
            items_in_wishlist = WishList.objects.filter(
                username=self.username)
            cart_items = []
            wishlist_items = []
            subtotal_cart = 0
            for item in items_in_cart:
                cart_items.append(Product.objects.get(name=item.item_name))
                subtotal_cart += ((Product.objects.get(name=item.item_name)
                                   ).price * item.quantity)
            for item in items_in_wishlist:
                wishlist_items.append(Product.objects.get(name=item.item_name))
            self.cart_count = len(cart_items)
            self.wishlist_count = len(wishlist_items)
            # items count in cart
            self.arguments['cart_count'] = self.cart_count
            # items count in wishlist
            self.arguments['wishlist_count'] = self.wishlist_count
            # Poduct Objects Matching If present in Cart
            self.arguments['cart_items'] = cart_items
            # Raw Cart Object Items
            self.arguments['items_in_cart'] = items_in_cart
            # Items in Wishlist
            self.arguments['wishlist_items'] = wishlist_items
            # Total Amount of the products in Cart
            self.arguments['subtotal_cart'] = subtotal_cart

        return render(request, self.template_name, self.arguments)

    def post(self, request, *args, **kwargs):
        self.username = request.user.username
        if self.username != "":
            items_in_cart = Cart.objects.filter(
                username=self.username)
            user = User.objects.get(username=self.username)
            first_name = request.POST.get("first-name")
            last_name = request.POST.get("last-name")
            email = request.POST.get("email")
            address = request.POST.get("address")
            city = request.POST.get("city")
            country = request.POST.get("country")
            zip_code = request.POST.get("zip_code")
            phone = request.POST.get("phone")
            payment_method = request.POST.get("payment_method")
            order = Order(username=user, first_name=first_name, last_name=last_name, email=email,
                          address=address, city=city, country=country, zip_code=zip_code, phone=phone)
            order.save()
            for item in items_in_cart:
                product = Product.objects.get(name=item.item_name)
                order_place = OrderBy(order_id=order.id, ordered_by=order, username=user,
                                      item=product, date_placed=date.today(), payment_type=payment_method)
                order_place.save()
            Cart.objects.filter(username=self.username).delete()

            subject = "Order Recieved - HomeShopping"
            message = """Thank You for shopping with Homeshopping.pk\n
                         Track your order """ + str(order.id) + """ id we hope you had a great time shopping with us !"""

            send_mail(subject, message, 'fakharudin99@gmail.com',[email])

            return render(request, 'thank-you.html', {"order_id": order.id, "email": email})
        else:
            return HttpResponseRedirect('/accounts/signup/')

        return render(request, self.template_name, self.arguments)


class Homepage(TemplateView):
    template_name = 'homepage.html'

    username = None
    products = Product.objects.all()
    categories = []
    subcategories = []
    for product in products:
        categories.append(product.category)
        subcategories.append(product.subcategory)
    categories = list(set(categories))
    categories.sort(key=lambda x: x.name.lower())
    subcategories = list(set(subcategories))
    subcategories.sort(key=lambda x: x.name.lower())
    cart_count = 0
    wishlist_count = 0

    arguments = {'products': products,
                 'categories': categories, 'subcategories': subcategories, 'cart_count': cart_count, 'wishlist_count': wishlist_count}

    def get(self, request, *args, **kwargs):
        self.username = request.user
        if "AnonymousUser" != self.username:
            if request.GET.get('type') == 'add-to-cart':
                item = request.GET.get('item')
                quantity = request.GET.get('qty')
                product = Product.objects.get(name=item)
                product.is_available -= int(quantity)
                product.save()
                if(self.check_existence_cart(self.username, item)):
                    cart_item = Cart.objects.get(
                        username=self.username, item_name=item)
                    cart_item.quantity += int(quantity)
                    cart_item.save()
                else:
                    form = Cart()
                    form.username = self.username
                    form.item_name = item
                    form.quantity = int(quantity)
                    form.save()
                return render(request, self.template_name, self.arguments)
            elif request.GET.get('type') == 'add-to-wishlist':
                item = request.GET.get('item')
                if not self.check_existence_wishlist(self.username, item):
                    form = WishList()
                    form.username = self.username
                    form.item_name = item
                    form.save()
                    return render(request, self.template_name, self.arguments)

                return render(request, self.template_name, self.arguments)
            elif request.GET.get('type') == 'delete-from-cart':
                item = request.GET.get('item')
                quantity = (Cart.objects.get(
                    username=self.username, item_name=item)).quantity
                product = Product.objects.get(name=item)
                product.is_available += quantity
                product.save()
                Cart.objects.filter(username=self.username,
                                    item_name=item).delete()
                return render(request, self.template_name, self.arguments)
            elif request.GET.get('type') == 'delete-from-wishlist':
                item = request.GET.get('item')
                WishList.objects.filter(item_name=item).delete()
                return render(request, self.template_name, self.arguments)

        items_in_cart = Cart.objects.filter(
            username=self.username)
        items_in_wishlist = WishList.objects.filter(
            username=self.username)
        cart_items = []
        wishlist_items = []
        subtotal_cart = 0
        for item in items_in_cart:
            cart_items.append(Product.objects.get(name=item.item_name))
            subtotal_cart += ((Product.objects.get(name=item.item_name)
                               ).price * item.quantity)
        for item in items_in_wishlist:
            wishlist_items.append(Product.objects.get(name=item.item_name))

        self.cart_count = len(cart_items)
        self.wishlist_count = len(wishlist_items)
        self.arguments['cart_count'] = self.cart_count  # items count in cart
        # items count in wishlist
        self.arguments['wishlist_count'] = self.wishlist_count
        # Poduct Objects Matching If present in Cart
        self.arguments['cart_items'] = cart_items
        # Raw Cart Object Items
        self.arguments['items_in_cart'] = items_in_cart
        self.arguments['wishlist_items'] = wishlist_items  # Items in Wishlist
        # Total of the products in Cart
        self.arguments['subtotal_cart'] = subtotal_cart
        return render(request, self.template_name, self.arguments)

    def check_existence_cart(self, username, item):
        product = Cart.objects.filter(username=username, item_name=item)
        amount = len(product)
        if amount:
            return True
        else:
            return False

    def check_existence_wishlist(self, username, item):
        product = WishList.objects.filter(username=username, item_name=item)
        amount = len(product)
        if amount:
            return True
        else:
            return False
