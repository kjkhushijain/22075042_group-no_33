from django.shortcuts import render, redirect,get_object_or_404
from .forms import UserForm, RegistrationForm, LoginForm, SelectionForm, DuesForm, NoDuesForm
from django.http import HttpResponse, Http404, HttpResponseForbidden
from selection.models import Student, Room, Hostel, Document,Warden, Complaint,ResolvedComplaint
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, ComplaintForm
from .models import Complaint
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.db.models import Q


User = get_user_model()


def home(request):
    return render(request, 'home.html')


def register(request):
    User = get_user_model()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
           
            student=Student.objects.create(user=new_user)
            student.no_dues = True
            student.save()
    
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password1'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('login/edit/')
                else:
                    return render(request, 'invalid_login.html')
            else:
                return HttpResponse('Authentication failed: Invalid username or password')
        else:
            return HttpResponse('Form is not valid: ' + str(form.errors))
    else:
        form = UserForm()
        args = {'form': form}
        return render(request, 'reg_form.html', args)

def user_login(request):
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password'])
           
            if user is not None:
                if user.is_warden:
                    return render(request, 'invalid_login.html')
               
                if user.is_active:
                    login(request, user)
                    student = request.user.student_profile
                    context={'student': student}
                    resolved_complaints=ResolvedComplaint.objects.all().order_by('-resolved_at')
                    context['resolved_complaints']=resolved_complaints
                    return render(request, 'profile.html', context)
                else:
                    return HttpResponse('Disabled account')
            else:
                return render(request, 'invalid_login.html')
        else:
            return render(request, 'invalid_login.html')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    
    
def warden_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password'])

            if user is not None:
                
                    if not user.is_warden:
                        return render(request, 'invalid_login.html')
                    if user.is_active:

                        login(request, user)
                        
                        room_list = request.user.warden.hostel.room_set.all()
                        students = Student.objects.filter(room__in=room_list)
                        context = {'rooms': room_list,'students':students}
                       
                        
                        return render(request, 'warden.html', context)
                    else:
                        print("User is not active")
                        return HttpResponse('Disabled account')
            else:
                print("Authentication failed")
                return render(request, 'invalid_login.html')
        else:
            print(form.errors)
            return render(request, 'invalid_login.html')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})




    
    
@login_required
def delete_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    if request.user == complaint.user:
        complaint.delete()
        
    return redirect('view_complaints')

@login_required
def update_complaint(request, complaint_id):
  complaint = get_object_or_404(Complaint, id=complaint_id)
  if request.user != complaint.user:
    return redirect('view_complaints')

  if request.method == 'POST':
    form = ComplaintForm(request.POST, instance=complaint)
    if form.is_valid():
      form.save()
      messages.success(request, 'Your complaint has been updated successfully.')
      return redirect('view_complaints')
  else:
    form = ComplaintForm(instance=complaint)

  return render(request, 'update_complaint.html', {'form': form})


def view_complaints(request):
    query = request.GET.get('q')
    if query:
        complaints = Complaint.objects.filter(Q(text__icontains=query) | Q(user__username__icontains=query)).order_by('-created')
    else:
        complaints = Complaint.objects.all().order_by('-created')
    for complaint in complaints:
    # Reverse the URL for the update_complaint view using the reverse_lazy() function
        update_complaint_url = reverse_lazy('update_complaint', args=(complaint.id,))

    # Add the update_complaint_url to the complaint object
        complaint.update_complaint_url = update_complaint_url
    return render(request, 'view_complaints.html', {'complaints':complaints})



def register_complaints(request):
  complaints = Complaint.objects.filter(status='New')
  for complaint in complaints:
    complaint.status = 'Registered'
    complaint.save()
  return redirect('view_complaints')



@login_required
def submit_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.status="New"
            complaint.user = request.user
            complaint.save()
            messages.success(request, 'Your complaint has been submitted successfully.')
            return redirect('view_complaints')
    else:
        form = ComplaintForm()
    
    return render(request, 'submit_complaint.html', {'form': form})



@login_required
def warden_view_complaints(request):
    # Check if the user is a warden
    if request.user.is_warden:
        # Get the warden associated with the user
        warden = Warden.objects.get(user=request.user)
        # Get the complaints for the warden's hostel
        complaints = Complaint.objects.filter(user__student_profile__hostel=warden.hostel).order_by('-created')
        return render(request, 'warden_view_complaints.html', {'complaints': complaints})
    else:
        return HttpResponseForbidden("You are not authorized to view this page.")


@login_required
def warden_delete_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    # Check if the logged in user is a warden and the complaint is under his hostel
    if request.user.is_warden and complaint.user.student_profile.hostel == request.user.warden.hostel:
        # Create a new ResolvedComplaint instance
        resolved_complaint = ResolvedComplaint(user=complaint.user, text=complaint.text)
        resolved_complaint.save()
        # Delete the complaint
        complaint.delete()
    else:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    return redirect('warden_view_complaints')

@login_required
def resolved_complaints(request):
    resolved_complaints = ResolvedComplaint.objects.all().order_by('-resolved_at')
    return render(request, 'resolved_complaints.html', {'resolved_complaints': resolved_complaints})







@login_required
def warden_dues(request):
    user = request.user
    try:
        warden = user.warden
    except Warden.DoesNotExist:
        return HttpResponse('Invalid Login')
    else:
        students = Student.objects.all()
        return render(request, 'dues.html', {'students': students})

@login_required
def warden_add_due(request):
  user = request.user
  try:
    warden = user.warden
  except Warden.DoesNotExist:
    return render(request, 'invalid_login.html')
  else:
    if request.method == "POST":
      form = DuesForm(request.POST)
      if form.is_valid():
        student = form.cleaned_data.get('student')
        amount = form.cleaned_data.get('amount')
        student.due_amount += amount
        student.no_dues = False if student.due_amount > 0 else True
        student.save()
        return HttpResponse('Done')
      else:
        # Re-render the form with the error messages.
        return render(request, 'add_due.html', {'form': form})
    else:
      # Initialize the form with only students under the current warden.
      form = DuesForm()
      form.fields['student'].queryset = Student.objects.filter(hostel=warden.hostel)
      return render(request, 'add_due.html', {'form': form})

@login_required
def warden_remove_due(request):
    user = request.user
    try:
        warden = user.warden
    except Warden.DoesNotExist:
        return render(request, 'invalid_login.html')
    else:
        if request.method == "POST":
            form = NoDuesForm(request.POST)
            if form.is_valid():
                student = form.cleaned_data.get('student')
                amount = form.cleaned_data.get('amount')
                student.due_amount -= amount
                student.no_dues = False if student.due_amount > 0 else True
                student.save()
                return HttpResponse('Done')
        else:
            form = NoDuesForm()
            # Modify the 'student' field label to include the due amount for each student.
            form.fields['student'].label_from_instance = lambda obj: "%s (Due amount: %s)" % (obj, obj.due_amount)
            return render(request, 'remove_due.html', {'form': form})


@login_required
def edit(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST,request.FILES ,instance=request.user.student_profile)
        if form.is_valid():
            form.save()
            student = request.user.student_profile
            return render(request, 'profile.html', {'student': student})
    else:
        form = RegistrationForm(instance=request.user.student_profile)
        return render(request, 'edit.html', {'form': form})
@login_required
def select(request):
    if request.user.student_profile.room:
        room_id_old = request.user.student_profile.room_id

    if request.method == 'POST':
        if not request.user.student_profile.no_dues:
            return HttpResponse('You have dues. Please contact your Hostel Caretaker or Warden')
        form = SelectionForm(request.POST, instance=request.user.student_profile)
        if form.is_valid():
            if request.user.student_profile.room_id:
                request.user.student_profile.room_allotted = True
                r_id_after = request.user.student_profile.room_id
                room = Room.objects.get(id=r_id_after)
                room.vacant = False
                room.save()
                try:
                    room = Room.objects.get(id=room_id_old)
                    room.vacant = True
                    room.save()
                except BaseException:
                    pass
            else:
                request.user.student_profile.room_allotted = False
                try:
                    room = Room.objects.get(id=room_id_old)
                    room.vacant = True
                    room.save()
                except BaseException:
                    pass
            form.save()
            student = request.user.student_profile
            return render(request, 'profile.html', {'student': student})
        else:
            return render(request, 'invalid_login.html')
    else:
        if not request.user.student_profile.no_dues:
            return HttpResponse('You have dues. Please contact your Hostel Caretaker or Warden')
        form = SelectionForm(instance=request.user.student_profile)
        student_gender = request.user.student_profile.gender
        student_course = request.user.student_profile.course
        student_room_type = request.user.student_profile.course.room_type
        hostel = Hostel.objects.filter(
            gender=student_gender, course=student_course)
        x = Room.objects.none()
        if student_room_type == 'B':
            for i in range(len(hostel)):
                h_id = hostel[i].id
                a = Room.objects.filter(
                    hostel_id=h_id, room_type__in=['S', 'D', 'B'], vacant=True)  # Include 'B' in the filter
                x = x | a
        else :
            for i in range(len(hostel)):
                h_id = hostel[i].id
                a = Room.objects.filter(
                    hostel_id=h_id, room_type=student_room_type, vacant=True)
                x = x | a
        form.fields["room"].queryset = x
        return render(request, 'select_room.html', {'form': form})




def logout_view(request):
    logout(request)
    return redirect('/')


def HOSTEL3(request):
    room_list = Room.objects.filter(hostel__name='HOSTEL3').order_by('name')
    room_dict = {'rooms':room_list}
    return render(request, 'hostel3.html', context=room_dict)


def HOSTEL2(request):
    room_list = Room.objects.filter(hostel__name='HOSTEL2').order_by('name')
    room_dict = {'rooms':room_list}
    return render(request, 'hostel2.html', context=room_dict)


def HOSTEL1(request):
    room_list = Room.objects.order_by('name')
    room_dict = {'rooms':room_list}
    return render(request, 'hostel1.html', context=room_dict)


def hostel_detail_view(request, hostel_name):
    try:
        this_hostel = Hostel.objects.get(name=hostel_name)
    except Hostel.DoesNotExist:
        raise Http404("Invalid Hostel Name")
    context = {
        'hostel': this_hostel,
        'rooms': Room.objects.filter(
            hostel=this_hostel)}
    return render(request, 'hostels.html', context)




def hostel_list(request):
    hostels = Hostel.objects.all()
    for hostel in hostels:
        hostel.menu = {}
        for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            try:
                hostel.menu[day] = hostel.get_day_menu_items(day)
            except  IndexError:
                pass
    context = {'hostels': hostels}
    return render(request, 'hostel_list.html', context)

def your_view(request):
    hostels = Hostel.objects.all()
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    return render(request, 'hostel_list.html', {'hostels': hostels, 'days': days})





