from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from django.db import models

from django.utils import timezone

# from django.contrib.auth.models import User


class User(AbstractUser):
    is_warden = models.BooleanField(default=False)






class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        default=None,
        null=True,
        on_delete=models.CASCADE,
        related_name="student_profile"
       )
    gender_choices = [('M', 'Male'), ('F', 'Female')]
    student_name = models.CharField(max_length=200, null=True)
    father_name = models.CharField(max_length=200, null=True)
    enrollment_no = models.CharField(max_length=10, unique=True, null=True)
    hostel = models.ForeignKey('Hostel', on_delete=models.SET_NULL, null=True, blank=True)
    student_image = models.ImageField(upload_to='student_images/', null=True, blank=True)
    course = models.ForeignKey(
        'Course',
        null=True,
        default=None,
        on_delete=models.CASCADE)
    dob = models.DateField(
        max_length=10,
        help_text="format : YYYY-MM-DD",
        null=True)
    gender = models.CharField(
        choices=gender_choices,
        max_length=1,
        default=None,
        null=True)
    room = models.OneToOneField(
        'Room',
        blank=True,
        on_delete=models.CASCADE,
        null=True,
        )
    document=models.FileField(upload_to='documents/',null=True)
    room_allotted = models.BooleanField(default=False)
    no_dues = models.BooleanField(default=True)
    due_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return self.student_name if self.student_name else "NO NAME"


class Room(models.Model):
    room_choice = [('S', 'Single Occupancy'), ('D', 'Double Occupancy'), ('P', 'Reserved for Research Scholars'),('B', 'Both Single and Double Occupancy')]
    no = models.CharField(max_length=5)
    name = models.CharField(max_length=10)
    room_type = models.CharField(choices=room_choice, max_length=1, default=None)
    vacant = models.BooleanField(default=True)
    hostel = models.ForeignKey('Hostel', on_delete=models.CASCADE)


    def __str__(self):
        return self.name


class Hostel(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    gender_choices = [('M', 'Male'), ('F', 'Female')]
    gender = models.CharField(
        choices=gender_choices,
        max_length=1,
        default=None,
        null=True)
    course = models.ManyToManyField('Course', default=None, blank=True)
    caretaker = models.CharField(max_length=100, blank=True)
    monday_menu = models.TextField(blank=True)
    tuesday_menu = models.TextField(blank=True)
    wednesday_menu = models.TextField(blank=True)
    thursday_menu = models.TextField(blank=True)
    friday_menu = models.TextField(blank=True)
    saturday_menu = models.TextField(blank=True)
    sunday_menu = models.TextField(blank=True)
    photo = models.ImageField(upload_to='documents/',default="default.jpg")
    def str(self):
        return self.name

    def get_day_menu_items(self, day):
        menu = getattr(self, f'{day}_menu').split('\n')
        breakfast = menu[0].split(':')[1].strip()
        lunch = menu[1].split(':')[1].strip()
        dinner = menu[2].split(':')[1].strip()
        return {'breakfast': breakfast, 'lunch': lunch, 'dinner': dinner} 

    def __str__(self):
        return self.name



    


class Course(models.Model):
    code = models.CharField(max_length=100, default=None)
    room_choice = [('S', 'Single Occupancy'), ('D', 'Double Occupancy'), ('P', 'Reserved for Research Scholars'), ('B', 'Both Single and Double Occupancy')]
    room_type = models.CharField(choices=room_choice, max_length=1, default='D')

    def __str__(self):
        return self.code



class Warden(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        default=None,
        null=True,
        on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=10, null=True)
    email = models.EmailField(max_length=254, null=True)
    hostel = models.ForeignKey('Hostel',
        default=None,
        null=True,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Document(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
class Complaint(models.Model):
    STATUS_CHOICES = [
        ('Submitted', 'Submitted'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
         ]


    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Submitted')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering = ['-updated', '-created']
    
  

    def _str_(self):
        return self.text[0:50]    

class ResolvedComplaint(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    resolved_at = models.DateTimeField(default=timezone.now)
