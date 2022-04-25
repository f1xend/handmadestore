from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, \
    Product, Category, ImageProduct, \
    ShoppingCart, ProductInShoppingCart, Order, ProductInOrder, StatusOrder


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'email',
        'surname',
        'first_name',
        'phone_number',
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'surname',
                'first_name',
                'phone_number',
                'is_staff',
                'is_active'
            )}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    class Meta:
        verbose_name_plural = 'Пользователи'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'cost',
    )


class ImageProductAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'title',
        'is_main',
        'image',
    )


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'sum_without_discount',
        'sum_with_discount',
        'date_created',
    )


class ProductInShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'shopping_cart',
        'product',
        'cost_without_discount',
        'cost_with_discount',
        'quantity',
        'final_cost',
    )


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'address',
        'date_created',
        # 'date_delivery',
        'shopping_cart',
    )


class ProductInOrderAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'product',
        'cost_without_discount',
        'cost_with_discount',
        'quantity',
        'final_cost',
    )


class StatusOrderAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'order',
        'status',
        'datetime_add',
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ImageProduct, ImageProductAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(ProductInShoppingCart, ProductInShoppingCartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductInOrder, ProductInOrderAdmin)
admin.site.register(StatusOrder, StatusOrderAdmin)
