from django.urls import path
from .views import (
    HomeView,

    AboutView,
    ContactView,
    SendMailView,
    
    CategoryView,
    MyOrderView,
    WriteReviewsView,
    MyReturnsView,
    CheckoutView,
    ItemDetailView,
    OrderSummaryView,
    PaymentView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart, 
    AddCouponView,    
    RequestRefundView, 
    SearchView,
    SubmitReviews,
    )

app_name = 'core'
urlpatterns=[
    path('', HomeView.as_view(), name='item-list'),
    
    path('about/', AboutView, name='AboutUs'),
    path('contact/', ContactView, name='ContactUs'),
    path('sendmail/', SendMailView, name='SendMail'),

    path('my-orders/', MyOrderView, name='my-orders'),
    path('category/<cat_name>', CategoryView, name='category-view'),
    path('write-reviews/<ref_code>/', WriteReviewsView, name='write-reviews'),
    path('submit-review/', SubmitReviews, name='submit-reviews'),
    path('my-returns/', MyReturnsView.as_view(), name='my-returns'),
    path('order-summary/', OrderSummaryView, name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('payment/<payment_option>/', PaymentView.as_view(), name="payment"),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove_single_item_from_cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name="payment"),
    path('request-refund/', RequestRefundView.as_view(), name="request-refund"),
    path('search/', SearchView.as_view(), name="search"),
    ]