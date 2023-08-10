from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReservationForm
from .models import Table, Reservation
from .forms import GuestRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from django.http import HttpResponse

def register(request):
    if request.method == 'POST':
        form = GuestRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = GuestRegistrationForm()
    return render(request, 'user/register.html', {'form': form})

def guest_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'user/login.html', {'error_message': 'Invalid login credentials.'})
    return render(request, 'user/login.html')

# @login_required(login_url='guest_login')
# def create_reservation(request):
#     if request.method == 'POST':
#         form = ReservationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('booking_success')
#     else:
#         form = ReservationForm()
#     return render(request, 'bookings/create_reservation.html', {'form': form})

def home(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            if request.user.is_authenticated:
                reservation.guest = request.user

            reservation.save()
            messages.success(request, 'Reservation created successfully!')
            return redirect('home')
    else:
        form = ReservationForm()
    return render(request, 'home.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def my_bookings(request):
    current_date = datetime.now().date()
    try:
        upcoming_reservations = Reservation.objects.filter(
            guest=request.user,
            date__gte=current_date,
            is_cancelled=False
        ).order_by('date', 'start_time')
    except Reservation.DoesNotExist:
        upcoming_reservations = {}
    return render(request, 'bookings/reservations.html', {'reservations': upcoming_reservations})

def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    if reservation.is_cancelled:
        return redirect('my_bookings')
    reservation.is_cancelled = True
    reservation.save()
    return redirect('my_bookings')