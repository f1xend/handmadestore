from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import ContextMixin

from main.models import Category, ProductInShoppingCart, ProductInOrder


class CategoriesMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ShoppingCartMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['products_in_sc'] = ProductInShoppingCart.objects \
                .filter(shopping_cart__user=self.request.user)
            if self.request.resolver_match\
                    .view_name == 'view_order_url' \
                    or self.request.resolver_match.view_name\
                    == 'admin_panel_order_url':
                context['products'] = ProductInOrder.objects.filter(
                        order=self.get_object()
                    )
                context['products'] = ProductInOrder.objects.filter(
                        order=self.get_object()
                    )
        else:
            context['products_in_sc'] = 'None'
        return context


