from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from datetime import datetime

import pytz


class CategoryModel(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('title'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class ProductModel(models.Model):
    category = models.ForeignKey(CategoryModel, on_delete=models.PROTECT, related_name='products',
                                 verbose_name=_('category'))
    brand = models.ForeignKey('BrandModel', on_delete=models.PROTECT, related_name='products', verbose_name=_('brand'))
    title = models.CharField(max_length=255, verbose_name=_('title'))
    image = models.ImageField(upload_to='products', verbose_name=_('image'))
    price = models.FloatField(verbose_name=_('price'))
    real_price = models.FloatField(verbose_name=_("real price"), default=0)
    discount = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],
                                           verbose_name=_('discount'))
    wishlist = models.ManyToManyField(User, related_name='wishlist', verbose_name='wishlist')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    @staticmethod
    def get_from_cart(request):
        cart = request.session.get('cart', [])
        price = ProductModel.objects.filter(pk__in=cart)
        return price

    def get_image(self):
        return self.image.url


    def get_related_products(self):
        # return self.category.products.exclude(pk=self.pk)
        return ProductModel.objects.filter(category_id=self.category_id).exclude(pk=self.pk)

    def __str__(self):
        return self.title

    def is_discount(self):
        return self.discount != 0

    def is_new(self):
        diff = datetime.now(pytz.timezone('Asia/Tashkent')) - self.created_at
        return diff.days <= 3

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')


class BrandModel(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('title'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('brand')
        verbose_name_plural = _('brands')

class ProductImageModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='images', verbose_name=_('product'))
    image = models.ImageField(upload_to='products', verbose_name=_('image'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = _('product image')
        verbose_name_plural = _('product images')
