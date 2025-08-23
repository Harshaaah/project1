# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.hashers import make_password



# class Client(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to built-in User
#     age = models.IntegerField(null=True, blank=True)
#     interest = models.CharField(max_length=255, blank=True)

#     def __str__(self):
#         return self.user.username



# class Counsellor(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to built-in User
#     age = models.IntegerField(null=True, blank=True)
#     experience = models.IntegerField(null=True, blank=True)

#     def __str__(self):
#         return self.user.username
# class Client(AbstractUser):
#     age = models.IntegerField(null=True, blank=True)
#     interest = models.CharField(max_length=255, blank=True)

#     def __str__(self):
#         return self.username

# class Counsellor(models.Model):
    
#     username = models.CharField(max_length=15, blank=True)
#     email = models.CharField(max_length=150, blank=True)
#     age = models.IntegerField(null=True, blank=True)
#     experience = models.IntegerField(null=True, blank=True)
#     def __str__(self):
#         return self.username

# class Counsellor(models.Model):
#     username = models.CharField(max_length=150, unique=True)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255, null=True, blank=True)  # will store hashed password
#     age = models.IntegerField(null=True, blank=True)
#     experience = models.IntegerField(null=True, blank=True)

#     def save(self, *args, **kwargs):
#         # Hash the password before saving
#         self.password = make_password(self.password)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.username
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_client = models.BooleanField(default=False)
    is_counsellor = models.BooleanField(default=False)

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client")
    age = models.IntegerField(null=True, blank=True)
    interest = models.CharField(max_length=255, blank=True)

class Counsellor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="counsellor")
    age = models.IntegerField(null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)

from .models import Client, Counsellor

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    counsellor = models.ForeignKey(Counsellor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.client.username} booked {self.counsellor.username} on {self.date} at {self.time}"
