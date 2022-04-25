import os
from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """
        Кастомный пользователь
    """

    username = models.CharField(
        max_length=20,
        db_index=True,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Имя пользователя'
    )

    email = models.EmailField(
        unique=True,
        db_index=True,
        verbose_name='E-mail адрес'
    )

    surname = models.CharField(
        blank=True,
        max_length=50,
        verbose_name='Фамилия',
    )

    first_name = models.CharField(
        blank=True,
        max_length=50,
        verbose_name='Имя',
    )

    phone_number = PhoneNumberField(
        null=True,
        blank=True,
        unique=True,
        verbose_name='Номер телефона'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.surname} {self.first_name} {self.email}'

    class Meta:
        ordering = ['-pk']

class Category(models.Model):
    """
        Категории
    """
    category = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name='Главная категория',
        null=True,
        blank=True,
        related_name='main_category'
    )

    title = models.CharField(
        max_length=50,
        verbose_name='Наименование категории'
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_list_url', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'Категории'


class Product(models.Model):
    """
        Продукт
    """

    title = models.CharField(
        max_length=200,
        verbose_name='Наименование товара'
    )

    description = models.CharField(
        max_length=500,
        verbose_name='Описание товара'
    )

    cost = models.DecimalField(
        verbose_name='Стоимость за ед.',
        decimal_places=2,
        max_digits=6
    )

    vendor_code = models.CharField(
        max_length=10,
        verbose_name='Артикул',
        default=None
    )

    characteristics = models.CharField(
        max_length=256,
        verbose_name='Характеристики',
        null=True,
        blank=True
    )

    category = models.ManyToManyField(
        Category,
        verbose_name='Категории',
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail_url', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'Товары'
        ordering = ['-pk']


class ImageProduct(models.Model):
    """
        Изображение продукта
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=50,
        verbose_name='Название изображения',
        null=True,
        blank=True
    )

    is_main = models.BooleanField(
        default=False,
        verbose_name='Это главное изображение?'
    )

    image = models.ImageField(
        upload_to='images/',
        verbose_name='Изображение'
    )

    def __str__(self):
        if self.title:
            return self.title
        return f'Изображение {self.pk}'

    def get_product_url(self):
        return reverse('product_detail_url', kwargs={'pk': self.product.pk})

    class Meta:
        verbose_name_plural = 'Изображения товаров'
        ordering = ['-pk']


# These two auto-delete files from filesystem when they are unneeded:
@receiver(models.signals.post_delete, sender=ImageProduct)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(models.signals.pre_save, sender=ImageProduct)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False
    try:
        old_file = ImageProduct.objects.get(pk=instance.pk).image
    except ImageProduct.DoesNotExist:
        return False
    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


class ShoppingCart(models.Model):
    """
        Корзина
    """

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    sum_without_discount = models.DecimalField(
        verbose_name='Сумма корзины без учета скидки',
        decimal_places=2,
        max_digits=6,
        null=True,
        blank=True
    )

    sum_with_discount = models.DecimalField(
        verbose_name='Сумма корзины с учетом скидки',
        null=True,
        decimal_places=2,
        max_digits=6,
        blank=True
    )

    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания корзины'
    )

    def __str__(self):
        return f'Корзина пользователя {self.user}'

    class Meta:
        verbose_name_plural = 'Корзины'


class AbstractPlaceProduct(models.Model):
    """
        Абстрактная модель для размещения товаров в корзине и заказе
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )

    cost_without_discount = models.DecimalField(
        verbose_name='Стоимость без учета скидки',
        decimal_places=2,
        max_digits=6,
        null=True,
        blank=True
    )

    cost_with_discount = models.DecimalField(
        verbose_name='Стоимость с учетом скидки',
        decimal_places=2,
        max_digits=6,
        null=True,
        blank=True
    )

    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество'
    )

    final_cost = models.DecimalField(
        verbose_name='Общая сумма',
        decimal_places=2,
        max_digits=6,
        null=True,
        blank=True
    )

    class Meta:
        abstract = True


class ProductInShoppingCart(AbstractPlaceProduct):
    """
        Товары в корзине
    """

    shopping_cart = models.ForeignKey(
        ShoppingCart,
        on_delete=models.CASCADE,
        verbose_name='Корзина'
    )

    def __str__(self):
        return f'{self.product} в {self.shopping_cart}'

    def save(self, *args, **kwargs):
        if self.cost_with_discount:
            self.final_cost = self.cost_with_discount * Decimal(self.quantity)
        elif self.cost_without_discount:
            self.final_cost = self.cost_without_discount * Decimal(self.quantity)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Товары в корзине'


class Order(models.Model):
    """
        Заказ
    """

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    address = models.CharField(
        max_length=350,
        verbose_name='Адрес',
        null=True,
    )

    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания заказа'
    )

    track_num = models.CharField(
        max_length=30,
        verbose_name='Трек номер',
        null=True,
        blank=True,
        default=''
    )

    shopping_cart = models.ForeignKey(
        ShoppingCart,
        on_delete=models.CASCADE,
        verbose_name='Корзина'
    )

    amount = models.DecimalField(
        verbose_name='Сумма заказа',
        decimal_places=2,
        max_digits=6,
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.user} от {self.date_created}'

    def get_success_url(self):
        return reverse('view_order_url', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-pk']
        verbose_name_plural = 'Заказы'


class ProductInOrder(AbstractPlaceProduct):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ'
    )

    def __str__(self):
        return f'{self.product} в {self.order}'

    class Meta:
        verbose_name_plural = 'Товары в заказе'


STATUS_CHOICES = [
    ('НП', 'Не подтвержден'),
    ('П', 'Принят'),
    ('О', 'Отправлен'),
    ('ПК', 'Принят клиентом'),
]


class StatusOrder(models.Model):
    status = models.CharField(
        choices=STATUS_CHOICES,
        verbose_name='Статус заказа',
        max_length=10
    )

    order = models.ForeignKey(
        Order,
        verbose_name='Заказ',
        on_delete=models.CASCADE
    )

    datetime_add = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.order}: {self.status}'

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказов'
