from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import MainView, ProductDetailView, ProductsListView, UserLoginView, UserPageView, AddProductInShoppingCart, \
    DelProductsInShoppingCart, DelProductInShoppingCart, AddOrder, OrderView, UserRegistrationView, AdminPanelPageView, \
    AdminPanelOrdersView, AdminPanelUsersView, AdminPanelUserOrdersView, AdminOrderView, AdminPanelProductsView, \
    AdminPanelAddProductView, AdminPanelProductView, AdminPanelAddImageView, EditQuanProductInShoppingCart, \
    AddAddressOrder, SetStatusOrder, SetTrackNum, DelProduct, AdminPanelEditProductView, AdminPanelEditProductPageView, \
    UserPageInfoView, UserUpdateInfoView, UserChangePasswordView, EditQuanProductInOrder, AdminPanelUpdateImageView, \
    AboutUsView, DeliveryView, DelProductView

urlpatterns = [
    path('', MainView.as_view(), name='main_url'),
    path('about-us', AboutUsView.as_view(), name='about_us_url'),
    path('delivery', DeliveryView.as_view(), name='delivery_url'),
    path('', MainView.as_view(), name='main_url'),
    path('products/<int:pk>', ProductsListView.as_view(), name='product_list_url'),
    path('products/product/<int:pk>', ProductDetailView.as_view(), name='product_detail_url'),
    path('shopping-card/add/<int:pk>', AddProductInShoppingCart.as_view(), name='add_prod_in_sc_url'),
    path('shopping-card/edit/quantity/<int:pk>', EditQuanProductInShoppingCart.as_view(), name='edit_quan_prod_in_sc_url'),
    path('shopping-card/delete/all', DelProductsInShoppingCart.as_view(), name='del_all_prod_in_sc_url'),
    path('shopping-card/delete/<int:pk>', DelProductInShoppingCart.as_view(), name='del_prod_in_sc_url'),
    path('order/create', AddOrder.as_view(), name='create_order_url'),
    path('order/create/address-add/<int:pk>', AddAddressOrder.as_view(), name='create_address_order_url'),
    path('order/<int:pk>', OrderView.as_view(), name='view_order_url'),
    path('user-page', UserPageView.as_view(), name='user_page_url'),
    path('user-page/info', UserPageInfoView.as_view(), name='user_page_info_url'),
    path('user-page/info/update', UserUpdateInfoView.as_view(), name='user_page_update_info_url'),
    path('user-page/password/', UserChangePasswordView.as_view(), name='user_password_change_url'),

    path('login', UserLoginView.as_view(), name='login_url'),
    path('logout', LogoutView.as_view(), name='logout_url'),
    path('registration', UserRegistrationView.as_view(), name='registration_url'),

    path('admin-panel', AdminPanelPageView.as_view(), name='admin_panel_url'),
    path('admin-panel/orders', AdminPanelOrdersView.as_view(), name='admin_panel_orders_url'),
    path('admin-panel/orders/order/<int:pk>', AdminOrderView.as_view(), name='admin_panel_order_url'),
    path('admin-panel/status-order/<int:pk>', SetStatusOrder.as_view(), name='set_status_order_url'),
    path('admin-panel/order/track-num/<int:pk>', SetTrackNum.as_view(), name='set_track_num_order_url'),
    path('admin-panel/order/quantity/o=<int:pk>&p=<int:product>', EditQuanProductInOrder.as_view(), name='edit_quan_order_url'),
    path('admin-panel/users', AdminPanelUsersView.as_view(), name='admin_panel_users_url'),
    path('admin-panel/users/user/<int:pk>', AdminPanelUserOrdersView.as_view(), name='admin_panel_user_orders_url'),
    path('admin-panel/products', AdminPanelProductsView.as_view(), name='admin_panel_products_url'),
    path('admin-panel/products/add', AdminPanelAddProductView.as_view(), name='add_product_admin_url'),
    path('admin-panel/products/edit/<int:pk>', AdminPanelEditProductView.as_view(), name='edit_product_admin_url'),
    path('admin-panel/products/edit/p=<int:pk>', AdminPanelEditProductPageView.as_view(), name='edit_product_p_admin_url'),
    path('admin-panel/products/delete/<int:pk>', DelProduct.as_view(), name='del_product_admin_url'),
    path('admin-panel/products/del/<int:pk>', DelProductView.as_view(), name='del_prod_admin_url'),
    path('admin-panel/products/product/<int:pk>', AdminPanelProductView.as_view(), name='product_admin_url'),
    path('admin-panel/products/product/<int:pk>/add-image', AdminPanelAddImageView.as_view(), name='add_product_image_admin_url'),
    path('admin-panel/products/product/<int:product>/edit-image/<int:pk>', AdminPanelUpdateImageView.as_view(), name='update_product_image_admin_url'),

]

