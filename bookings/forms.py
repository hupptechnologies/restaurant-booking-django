from django import forms
from django.core.exceptions import ValidationError
from .models import Reservation, Table
from django.contrib.auth.models import User
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput

class GuestRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise forms.ValidationError("Email field is required.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class ReservationForm(forms.ModelForm):
    table = forms.ModelChoiceField(queryset=Table.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Table'}))
    customer_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Name'}))
    # date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Select Date'}))
    # start_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Select Start Time'}))
    # end_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Select End Time'}))
    date = forms.DateField(
        widget=DatePickerInput(
            options={
                "format": "YYYY-MM-DD",
                "showClose": True,
                "showClear": True,
                "showTodayButton": True,
            },
            attrs={'class': 'form-control', 'placeholder': 'Select Date'}
        )
    )
    start_time = forms.TimeField(
        widget=TimePickerInput(attrs={'class': 'form-control', 'placeholder': 'Select Start Time'})
    )
    end_time = forms.TimeField(
        widget=TimePickerInput(attrs={'class': 'form-control', 'placeholder': 'Select End Time'})
    )

    class Meta:
        model = Reservation
        fields = ['table', 'customer_name', 'date', 'start_time', 'end_time']

    def clean(self):
        cleaned_data = super().clean()
        table = cleaned_data.get('table')
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if table and date and start_time and end_time:
            conflicting_reservations = Reservation.objects.filter(
                table=table,
                date=date,
                start_time__lt=end_time,
                end_time__gt=start_time
            )
            if self.instance:
                conflicting_reservations = conflicting_reservations.exclude(pk=self.instance.pk)
            if conflicting_reservations.exists():
                raise ValidationError("Another reservation already exists for the selected date and time range.")

        return cleaned_data