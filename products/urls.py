from django.urls import path
from . import views


urlpatterns = [
    path('item/<str:name>', views.ItemClass.as_view(), name='item'),
    path('brands/<str:name>', views.BrandsClass.as_view(), name='brands'),
    path('category/<str:name>', views.CategoryClass.as_view(), name='category'),
]
