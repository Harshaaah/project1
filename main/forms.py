from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.core.exceptions import ValidationError
from .models import User, Client, Counsellor, Booking


# -------------------
# CLIENT REGISTRATION
# -------------------
INTEREST_CHOICES = [
    ('career', 'Career'),
    ('finance', 'Finance'),
    ('relationship', 'Relationship'),
    ('health', 'Health'),
]

class ClientRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    age = forms.IntegerField(required=False)
    interest = forms.MultipleChoiceField(
        choices=INTEREST_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = User   # IMPORTANT: use your custom User
        fields = ['username', 'email', 'password1', 'password2', 'age', 'interest']


    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_client = True   # mark as client
        if commit:
            user.save()
            # Save Client profile
            Client.objects.create(
                user=user,
                age=self.cleaned_data['age'],
                interest=", ".join(self.cleaned_data['interest'])  # store as string
            )
        return user


# ----------------------
# COUNSELLOR REGISTRATION
# ----------------------
class CounsellorRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    age = forms.IntegerField(required=False)
    experience = forms.IntegerField(required=False)

    class Meta:
        model = User   # also use custom User
        fields = ['username', 'email', 'password1', 'password2', 'age', 'experience']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_counsellor = True   # mark as counsellor
        if commit:
            user.save()
            Counsellor.objects.create(
                user=user,
                age=self.cleaned_data['age'],
                experience=self.cleaned_data['experience']
            )
        return user


# ----------------------
# BOOKING FORM
# ----------------------
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['counsellor', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
