
from django.urls import path

from .import views
from .views import (
                   add_to_cart, add_to_wish, remove_from_cart,
                    remove_single_item_from_cart,
                    Paypal, remove_from_wish, CategoryDetail, ContactView,
                    Login, Faq, Text, Accounts, SearchView
                    )
app_name = 'eco'

urlpatterns = [

    path('product/',views.EcoIndex.as_view(), name='EcoIndex'),

    path('checkout/',views.Checkout.as_view(), name='checkout'),

    path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
    path('wish-summary/', views.WishSummaryView.as_view(), name='wish-summary'),

    path('account/', views.Accounts.as_view(), name='account-summary'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('product/<slug>/',views.EcoDetail.as_view(), name='EcoDetail'),

    path('category/<slug>/',views.CategoryDetail.as_view(), name='CategoryDetail'),

    path('add_to_cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', views.AddCouponView.as_view(), name='add-coupon'),

    path('remove_from_cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove_single_item_from_cart/<slug>/', remove_single_item_from_cart, name='remove_single_item_from_cart'),

    path('add_to_wish/<slug>/', add_to_wish, name='add-to-wish'),
    path('remove_from_wish/<slug>/', remove_from_wish, name='remove-to-wish'),

    path('payment/<payment_option>/', views.PaymentView.as_view(), name='payment'),

    path('paypal/', views.Paypal.as_view(), name='paypal'),
    path('login/', views.Login.as_view(), name='login'),

    path('contact/', views.ContactView.as_view(), name='contact'),
    path('faq/', views.Faq.as_view(), name='faq'),
    path('text/', views.Text.as_view(), name='text')


]

