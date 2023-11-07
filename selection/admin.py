from django import forms
from django.contrib import admin
from .models import Student, Room, Hostel, Course, User, Warden, Document

class UserAdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = '__all__'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ['is_warden','username']


admin.site.register(User, UserAdmin)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'student_name',
        'father_name',
        'gender',
        'enrollment_no',
        'course',
        'dob',
        'room',
        'room_allotted']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['no', 'name', 'room_type', 'vacant', 'hostel']

@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'room_type']

@admin.register(Warden)
class WardenAdmin(admin.ModelAdmin):
    list_display = ['name']
    
admin.site.register(Document)