from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetConfirmView, PasswordChangeView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView, DeleteView
from django.views.generic.base import View, TemplateView
from main.forms import CustomAuthenticationForm, CustomUserCreationForm, ProductForm, ImageForm, OrderForm, \
    StatusOrderForm, TrackNumForm, CustomUserChangeForm, CustomSetPasswordForm, ChangeQuanForm
from main.mixins import CategoriesMixin, ShoppingCartMixin
from main.models import Product, ImageProduct, Category, Order, \
    ProductInShoppingCart, ShoppingCart, ProductInOrder, CustomUser, StatusOrder


class MainView(CategoriesMixin, ShoppingCartMixin, ListView):
    """
    Просмотр главной страницы view
    """
    template_name = 'main/main.html'
    context_object_name = 'cards'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        categories = Category.objects.all()
        arr = []
        for category in categories:
            queryset = ImageProduct.objects \
                           .select_related('product') \
                           .filter(is_main=True) \
                           .filter(product__category__pk=category.pk)[:4]
            arr.append({'category': category, 'queryset': queryset})
        context['arr'] = arr
        context['categories'] = categories
        return context

    def get_queryset(self):
        qs = ImageProduct.objects.none()
        return qs


class ProductsListView(ShoppingCartMixin, CategoriesMixin, ListView):
    """
    Просмотр списка товаров view
    """
    template_name = 'main/products/products.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['category'] = category
        return context

    def get_queryset(self):
        qs = ImageProduct.objects.select_related('product') \
            .filter(is_main=True) \
            .filter(product__category__pk=self.kwargs['pk'])
        return qs


class ProductDetailView(ShoppingCartMixin, CategoriesMixin, DetailView):
    """
    Просмотр товара view
    """
    template_name = 'main/products/product.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        obj = ImageProduct.objects.select_related('product').filter(is_main=True).get(product=self.kwargs['pk'])
        return obj


# Личный кабинет пользователя
class UserPageView(ShoppingCartMixin, CategoriesMixin, LoginRequiredMixin, ListView):
    template_name = 'main/personal_area/user_page.html'
    context_object_name = 'orders'

    def get_queryset(self):
        qs = Order.objects.filter(user=self.request.user)
        return qs


# Личный кабинет информация пользователя
class UserPageInfoView(ShoppingCartMixin, CategoriesMixin, LoginRequiredMixin, TemplateView):
    template_name = 'main/personal_area/user_info.html'

    def get_context_data(self, **kwargs):
        context = super(UserPageInfoView, self).get_context_data(**kwargs)
        context['user'] = CustomUser.objects.get(
            pk=self.request.user.pk
        )

        return context


# Личный кабинет обновить информацию пользователя
class UserUpdateInfoView(ShoppingCartMixin, CategoriesMixin, LoginRequiredMixin, UpdateView):
    template_name = 'main/personal_area/user_edit.html'
    form_class = CustomUserChangeForm

    def get_object(self, queryset=None):
        obj = CustomUser.objects.get(pk=self.request.user.pk)
        return obj

    def get_success_url(self):
        return reverse('user_page_info_url')


# Личный кабинет обновить информацию пользователя
class UserChangePasswordView(ShoppingCartMixin, CategoriesMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/personal_area/user_change_password.html'
    form_class = CustomSetPasswordForm

    def get_success_url(self):
        return reverse('user_page_info_url')


# AdminPanel PermissionsMixin,
class AdminPanelPageView(ShoppingCartMixin, CategoriesMixin, LoginRequiredMixin, TemplateView):
    template_name = 'main/adminpanel/admin.html'

    def get_context_data(self, **kwargs):
        context = super(AdminPanelPageView, self).get_context_data(**kwargs)
        context['orders_count'] = Order.objects.all().count()
        context['users_count'] = CustomUser.objects.all().count()
        context['products_count'] = Product.objects.all().count()

        return context


# AdminPanel заказы PermissionsMixin,
class AdminPanelOrdersView(ShoppingCartMixin, CategoriesMixin, LoginRequiredMixin, ListView):
    template_name = 'main/adminpanel/orders/orders.html'
    context_object_name = 'orders'
    paginate_by = 8

    def get_queryset(self):
        qs = Order.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super(AdminPanelOrdersView, self).get_context_data(**kwargs)
        search_query = self.request.GET.get('search', '')
        if search_query:
            qs = Order.objects.select_related('user').filter(
                Q(user__email__icontains=search_query)
                | Q(date_created__icontains=search_query)
                | Q(pk__icontains=search_query)
                | Q(track_num__icontains=search_query)
                | Q(address__icontains=search_query)).distinct()
        else:
            qs = self.get_queryset()
        paginator = Paginator(qs, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            orders_p = paginator.page(page)
        except PageNotAnInteger:
            orders_p = paginator.page(1)
        except EmptyPage:
            orders_p = paginator.page(paginator.num_pages)

        context['orders_p'] = orders_p
        context['search_query'] = search_query

        return context


# AdminPanel Пользователи PermissionsMixin,
class AdminPanelUsersView(ShoppingCartMixin, CategoriesMixin, LoginRequiredMixin, ListView):
    template_name = 'main/adminpanel/users/users.html'
    context_object_name = 'users'
    paginate_by = 8

    def get_queryset(self):
        qs = CustomUser.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super(AdminPanelUsersView, self).get_context_data(**kwargs)
        search_query = self.request.GET.get('search', '')
        if search_query:
            qs = CustomUser.objects.filter(
                Q(email__icontains=search_query)
                | Q(first_name__icontains=search_query)
                | Q(phone_number__icontains=search_query)
                | Q(surname__icontains=search_query)).distinct()
        else:
            qs = self.get_queryset()
        paginator = Paginator(qs, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            users_p = paginator.page(page)
        except PageNotAnInteger:
            users_p = paginator.page(1)
        except EmptyPage:
            users_p = paginator.page(paginator.num_pages)

        context['users_p'] = users_p
        context['search_query'] = search_query
        return context


# AdminPanel Просмотр заказов пользователя PermissionsMixin,
class AdminPanelUserOrdersView(ShoppingCartMixin, CategoriesMixin, LoginRequiredMixin, ListView):
    template_name = 'main/adminpanel/users/user_orders.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        qs = Order.objects.filter(
            user__pk=self.kwargs['pk']
        )
        return qs

    def get_context_data(self, **kwargs):
        context = super(AdminPanelUserOrdersView, self).get_context_data(**kwargs)
        qs = self.get_queryset()
        paginator = Paginator(qs, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            orders_p = paginator.page(page)
        except PageNotAnInteger:
            orders_p = paginator.page(1)
        except EmptyPage:
            orders_p = paginator.page(paginator.num_pages)

        context['orders_p'] = orders_p
        return context


# Просмотр заказа
class OrderView(LoginRequiredMixin, ShoppingCartMixin, CategoriesMixin, DetailView):
    template_name = 'main/orders/order.html'
    context_object_name = 'order'

    def get_object(self, queryset=None):
        obj = Order.objects.get(pk=self.kwargs['pk'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = StatusOrder.objects.filter(
            order=self.get_object()
        ).last()
        return context


# Просмотр заказа через Админку
class AdminOrderView(OrderView):
    template_name = 'main/adminpanel/orders/order.html'
    context_object_name = 'order'

    def get_object(self, queryset=None):
        obj = Order.objects.get(pk=self.kwargs['pk'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = StatusOrder.objects.filter(
            order=self.get_object()
        ).last()
        context['form_status'] = StatusOrderForm()
        context['form_track_num'] = TrackNumForm()
        return context


# Установить статус заказа
class SetStatusOrder(ShoppingCartMixin, CategoriesMixin, LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        form_status = StatusOrderForm(request.POST)
        if request.user.is_superuser and form_status.is_valid():
            status_order = form_status.save(commit=False)
            status_order.order = Order.objects.get(pk=self.kwargs['pk'])
            status_order.save()
            return redirect('admin_panel_order_url', pk=self.kwargs['pk'])


# Установить трек номер заказа
class SetTrackNum(ShoppingCartMixin, CategoriesMixin, LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        form_track_num = TrackNumForm(request.POST)
        if request.user.is_superuser and form_track_num.is_valid():
            track_num = form_track_num.save(commit=False).track_num
            order.track_num = track_num
            order.save()
            return redirect('admin_panel_order_url', pk=self.kwargs['pk'])


# Просмотр товаров
class AdminPanelProductsView(ShoppingCartMixin, CategoriesMixin, LoginRequiredMixin, ListView):
    template_name = 'main/adminpanel/products/products.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_queryset(self):
        qs = Product.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super(AdminPanelProductsView, self).get_context_data(**kwargs)
        search_query = self.request.GET.get('search', '')
        if search_query:
            qs = Product.objects.filter(
                Q(title__icontains=search_query)
                | Q(vendor_code__icontains=search_query)).distinct()
        else:
            qs = self.get_queryset()
        paginator = Paginator(qs, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            products_p = paginator.page(page)
        except PageNotAnInteger:
            products_p = paginator.page(1)
        except EmptyPage:
            products_p = paginator.page(paginator.num_pages)

        context['products_p'] = products_p
        context['search_query'] = search_query
        return context


# Добавление товара через админку
class AdminPanelAddProductView(LoginRequiredMixin, FormView):
    template_name = 'main/adminpanel/products/add_product.html'
    form_class = ProductForm

    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('add_product_image_admin_url', pk=product.pk)


# Редактирование товара через админку
class AdminPanelEditProductView(LoginRequiredMixin, UpdateView):
    template_name = 'main/adminpanel/products/add_product.html'
    form_class = ProductForm

    def get_object(self, queryset=None):
        obj = Product.objects.get(pk=self.kwargs['pk'])
        return obj

    def get_success_url(self):
        return reverse('admin_panel_products_url')


# Редактирование товара через админку из страницы товара
class AdminPanelEditProductPageView(AdminPanelEditProductView):
    def get_success_url(self):
        return reverse('product_admin_url', kwargs={'pk': self.kwargs['pk']})


# Добавление фотографии товару через админку
class AdminPanelAddImageView(LoginRequiredMixin, FormView):
    template_name = 'main/adminpanel/products/add_image.html'
    form_class = ImageForm

    def post(self, request, *args, **kwargs):
        form = ImageForm(request.POST, request.FILES)
        product = Product.objects.get(pk=self.kwargs['pk'])
        if form.is_valid():
            image = form.save(commit=False)
            image.product = product
            image.save()
            return redirect('product_admin_url', pk=product.pk)
        else:
            return redirect('product_admin_url', pk=product.pk)


# Добавление фотографии товару через админку
class AdminPanelUpdateImageView(LoginRequiredMixin, UpdateView):
    template_name = 'main/adminpanel/products/add_image.html'
    form_class = ImageForm

    def get_object(self, queryset=None):
        obj = ImageProduct.objects.get(
            pk=self.kwargs['pk']
        )
        return obj

    def get_success_url(self):
        return reverse('product_admin_url', kwargs={'pk': self.kwargs['product']})


# Просмотр товара через админку
class AdminPanelProductView(LoginRequiredMixin, DetailView):
    template_name = 'main/adminpanel/products/product.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        obj = Product.objects.get(
            pk=self.kwargs['pk']
        )
        return obj

    def get_context_data(self, **kwargs):
        context = super(AdminPanelProductView, self).get_context_data(**kwargs)
        try:
            image = ImageProduct.objects.get(
                product=self.kwargs['pk']
            )
        except ImageProduct.DoesNotExist:
            image = ImageProduct.objects.none()
        context['image'] = image

        return context


# Авторизация пользователя
class UserLoginView(CategoriesMixin, LoginView):
    template_name = 'main/personal_area/login.html'
    success_url = 'user_page_url'
    redirect_authenticated_user = True
    form_class = CustomAuthenticationForm


# Регистрация пользователя
class UserRegistrationView(CategoriesMixin, FormView):
    template_name = 'main/personal_area/registration.html'
    success_url = reverse_lazy('user_page_url')
    redirect_authenticated_user = True
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        form.save()
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password1']
        )
        login(self.request, user)
        return super(UserRegistrationView, self).form_valid(form)


# Добавить товар в корзину
class AddProductInShoppingCart(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            sc = ShoppingCart.objects.select_related('user').get(user=self.request.user.pk)
            product = Product.objects.get(
                pk=self.kwargs['pk']
            )

            try:
                p = ProductInShoppingCart.objects.get(
                    shopping_cart=sc.pk,
                    product=product.pk,
                )

                p.quantity += 1
                p.save()
            except ProductInShoppingCart.DoesNotExist:
                ProductInShoppingCart.objects.create(
                    shopping_cart=sc,
                    product=product,
                    cost_without_discount=product.cost,
                    quantity=1,
                )
            return HttpResponseRedirect(self.request.META['HTTP_REFERER'])
        else:
            return redirect('login_url')


# Изменить количество товара в корзине
class EditQuanProductInShoppingCart(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            sc = ShoppingCart.objects.select_related('user').get(user=self.request.user.pk)
            product = Product.objects.get(
                pk=self.kwargs['pk']
            )
            if self.request.POST['quantity'] == '0':
                return HttpResponseRedirect(self.request.META['HTTP_REFERER'])
            else:
                try:
                    p = ProductInShoppingCart.objects.get(
                        shopping_cart=sc.pk,
                        product=product.pk,
                    )
                    p.quantity = int(request.POST.get('quantity'))
                    p.save()
                except ProductInShoppingCart.DoesNotExist:
                    ProductInShoppingCart.objects.create(
                        shopping_cart=sc,
                        product=product,
                        cost_without_discount=product.cost,
                        quantity=request.POST.get('quantity'),
                    )
                return HttpResponseRedirect(self.request.META['HTTP_REFERER'])
        else:
            return redirect('login_url')


# Изменить количество товара в заказе
class EditQuanProductInOrder(UpdateView):
    template_name = 'main/adminpanel/orders/change_quan.html'
    form_class = ChangeQuanForm

    def post(self, request, *args, **kwargs):
        order = Order.objects.select_related('user').get(pk=self.kwargs['pk'])
        form = ChangeQuanForm(request.POST)
        amount = 0
        old_amount = 0

        p_in_order = form.save(commit=False)
        p = self.get_object()
        old_quan = p.quantity
        old_final_cost_product = p.final_cost
        p.quantity = p_in_order.quantity
        if p.cost_with_discount:
            p.final_cost = p.quantity * p.cost_with_discount
        elif p.cost_without_discount:
            p.final_cost = p.quantity * p.cost_without_discount
        p.save()
        order.amount -= old_final_cost_product
        order.amount += p.final_cost
        order.save()
        return redirect(self.get_success_url())

    def get_object(self, queryset=None):
        order = Order.objects.select_related('user').get(pk=self.kwargs['pk'])
        product = Product.objects.get(
            pk=self.kwargs['product']
        )
        product_in_order = ProductInOrder.objects.get(
            order=order,
            product=product,
        )
        return product_in_order

    def get_success_url(self):
        return reverse('admin_panel_order_url', kwargs={'pk': self.kwargs['pk']})


# Удалить товар из корзины
class DelProductInShoppingCart(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        sc = ShoppingCart.objects.select_related('user').get(user=self.request.user.pk)
        product = Product.objects.get(
            pk=self.kwargs['pk']
        )
        ProductInShoppingCart.objects.get(
            shopping_cart=sc,
            product=product
        ).delete()
        return HttpResponseRedirect(self.request.META['HTTP_REFERER'])


# Очистить корзину
class DelProductsInShoppingCart(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        sc = ShoppingCart.objects.select_related('user').get(user=self.request.user.pk)
        ProductInShoppingCart.objects.filter(
            shopping_cart=sc
        ).delete()
        return HttpResponseRedirect(self.request.META['HTTP_REFERER'])


# Добавить заказ
class AddOrder(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        sc = ShoppingCart.objects.select_related('user').get(user=self.request.user.pk)
        products_in_sc = ProductInShoppingCart.objects.filter(
            shopping_cart=sc,
        )
        order = Order.objects.create(
            user=self.request.user,
            shopping_cart=sc
        )
        amount = 0
        for product_in_sc in products_in_sc:
            amount += product_in_sc.final_cost
            ProductInOrder.objects.create(
                product=product_in_sc.product,
                order=order,
                cost_without_discount=product_in_sc.product.cost,
                quantity=product_in_sc.quantity,
                final_cost=product_in_sc.final_cost
            )

        order.amount = amount
        order.save()
        status = StatusOrder.objects.create(
            order=order,
            status='НП',
        )
        status.save()
        products_in_sc.delete()

        return redirect('create_address_order_url', pk=order.pk)


# Добавить адрес заказа
class AddAddressOrder(LoginRequiredMixin, FormView):
    template_name = 'main/orders/add_address_order.html'
    form_class = OrderForm

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.get(
                pk=self.kwargs['pk']
            )
            o = form.save(commit=False)
            order.address = o.address
            order.save()
            return redirect('view_order_url', pk=order.pk)


class DelProduct(ShoppingCartMixin, CategoriesMixin, LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            Product.objects.get(
                pk=self.kwargs['pk']
            ).delete()
        return HttpResponseRedirect(self.request.META['HTTP_REFERER'])


class DelProductView(LoginRequiredMixin, DeleteView):
    template_name = 'main/adminpanel/products/product_delete_confirmation.html'

    def get_object(self, queryset=None):
        if self.request.user.is_superuser:
            obj = Product.objects.get(
                pk=self.kwargs['pk']
            )
        else:
            obj = Product.objects.none
        return obj

    def get_success_url(self):
        return reverse('admin_panel_products_url')

    # def post(self, request, *args, **kwargs):
    #     if request.user.is_superuser:
    #         Product.objects.get(
    #             pk=self.kwargs['pk']
    #         ).delete()
    #     return HttpResponseRedirect(self.request.META['HTTP_REFERER'])


class AboutUsView(ShoppingCartMixin, CategoriesMixin, TemplateView):
    template_name = 'main/about_us/about_us.html'


class DeliveryView(ShoppingCartMixin, CategoriesMixin, TemplateView):
    template_name = 'main/about_us/delivery.html'
