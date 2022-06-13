from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model

User = get_user_model()

SPECIALIZATION_CHOICES = (
    ("Dentist", "Dentist"),
    ("Surgeon", "Surgeon"),
    ("Nose, Throat & Ear", "Nose, Throat & Ear"),
    ("Pediatrics", "Pediatrics"),
    ("Orthopedics", "Orthopedics"),
)

GENDER_CHOICES = (
    ("MALE", "MALE"),
    ("FEMALE", "FEMALE"),
)


class Specialization(models.Model):
    spec_name = models.CharField(max_length=40, choices=SPECIALIZATION_CHOICES)

    def __str__(self):
        return self.spec_name


class Address(models.Model):
    street = models.CharField(max_length=50)
    house_flat_no = models.CharField(max_length=50)
    locality = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)


class Doctor(models.Model):
    user = models.OneToOneField(
        User, related_name="user_doctor", on_delete=models.CASCADE
    )
    registeration = models.CharField(max_length=30, blank=True, null=True)
    specialization = models.CharField(
        max_length=40, choices=SPECIALIZATION_CHOICES, default=None
    )
    education = models.CharField(max_length=100, null=False, blank=False)
    practicing_since = models.DateField(null=False, blank=False)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, null=False, blank=False
    )
    profile_pic = models.CharField(
        max_length=500,
        default="https://mpcthospital.in/wp-content/uploads/2019/02/doctor-profile-350x350.png",
    )
    verified = models.BooleanField(default=False)
    clinic = models.ForeignKey(
        Address,
        related_name="address_doctor",
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
    )

    def __str__(self):
        return self.user.first_name


# from django.db import models

# # Create your models here.
# from django.contrib.auth import get_user_model
# User = get_user_model()

# GENDER_CHOICES = (('MALE', 'MALE'), ('FEMALE', 'FEMALE'),)

# class Specialization(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class Place(models.Model):
#     name = models.CharField(max_length=100)
#     address_line_1 = models.CharField(max_length=300)
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     pincode = models.CharField(max_length=6)
#     latitude = models.CharField(max_length=20)
#     longitude = models.CharField(max_length=20)

#     def __str__(self):
#         return self.name

# class ClinicTimings(models.Model):
#     start_time = models.CharField(max_length=20)
#     end_time = models.CharField(max_length=20)

# class Services(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class NameYears(models.Model):
#     name = models.CharField(max_length=100)
#     start_year = models.CharField(max_length=4)
#     end_year = models.CharField(max_length=4)

#     def __str__(self):
#         return self.name


# class Doctor(models.Model):
#     name = models.CharField(max_length=100)
#     specializations = models.ManyToManyField(Specialization)
#     main_specialization = models.ForeignKey(Specialization, on_delete=models.DO_NOTHING, related_name="doctor_specialization")
#     yoe = models.FloatField(default=0)
#     about = models.TextField()
#     clinic = models.ForeignKey(Place, related_name="doctor_clinic", on_delete=models.DO_NOTHING)
#     timings = models.ManyToManyField(ClinicTimings)
#     fees = models.FloatField(default=100)
#     appointment_booking = models.BooleanField(default=False)
#     services = models.ManyToManyField(Services)
#     awards_recognitions = models.ManyToManyField(NameYears)
#     education = models.ForeignKey(NameYears, related_name="doctor_education", on_delete=models.CASCADE)
#     work_experience = models.ManyToManyField(NameYears)
