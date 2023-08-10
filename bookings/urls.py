from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.guest_login, name='guest_login'),
    path('logout/', views.logout_view, name='logout'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    # path('create/', views.create_reservation, name='create_reservation'),
    # path('success/', views.booking_success, name='booking_success'),
    path('cancel/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
]