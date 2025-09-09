from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from users.forms import CustomRegistrationForm, CustomLoginForm, CreateGroupForm,GroupUpdateSelectForm, AssignRoleForm, CustomUserUpdateForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from events.views import all_count, is_organizer
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from events.models import EventModel


def is_admin(user):
    return user.groups.filter(name="Admin").exists()

def is_participant(user):
    return user.groups.filter(name="Participants").exists()

# Create your views here.
def sign_up(request):
    
    form = CustomRegistrationForm()
    
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active = False
            
            form.save()
            messages.success(request, 'Registration Successful. \n\n A varification mail send on your email.')
            return redirect('sign-in')
        else:
            messages.warning(request, "Registration Unsuccessfull!!")
    
    return render(request, 'users_form/registration.html', {"form" : form})

def sign_in(request):
    form = CustomLoginForm()
    
    if request.method == 'POST':
        form = CustomLoginForm(data = request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request,'Login Successfull.')
            return redirect('redirect-dashboard')
    return render(request, 'users_form/login.html', {"form" : form})

@login_required(login_url='sign-in')
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        
    return redirect('home')

def active_account(request, user_id, token):
    try:
        user = User.objects.get(id = user_id)
        if default_token_generator.check_token(user,token):
            user.is_active = True
            user.save()
            messages.success(request, "Account activated.")
        else:
            return HttpResponse('Token Invalid!!')
    except user.DoesNotExist:
        return HttpResponse('User does not exist!!')
            
    return redirect('sign-in')
    
@user_passes_test(is_admin, login_url='no-parmission')
def admin_dashboard(request):
    users = User.objects.all()
    
    aflag = is_admin(request.user)
    
    count = all_count()
    context ={
        "users" : users,
        "count" : count,
        "aflag" : aflag,
        }
    
    return render(request, 'admin/dashboard.html', context)  

@login_required(login_url='sign-in')
@user_passes_test(is_admin, login_url='no-parmission')
def create_group(request):
    form = CreateGroupForm()
    
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        group = form.save()
        messages.success(request, f"{group.name} Role assign Successfull.")
        return redirect('create-group')
    
    return render(request, 'admin/create_group.html', {"form" : form, "gflag" : True})


@login_required(login_url='sign-in')
@user_passes_test(is_admin, login_url='no-parmission')
def update_group_data(request, group_id):
    

    group = get_object_or_404(Group, id = group_id)
    
    form = CreateGroupForm(instance = group)
    
    if request.method == 'POST':
        form = CreateGroupForm(request.POST, instance = group)
        form.name = group.name
        form.save()
        messages.success(request,"Group update successfully.")
        return redirect('view-group')
    
    context = {
        "form" : form,
        }
    return render(request, 'admin/create_group.html', context)

@login_required(login_url='sign-in')
@user_passes_test(is_admin, login_url='no-parmission')
def view_group_update_list(request):
    groups = Group.objects.all()
    return render(request, 'admin/view_update_group_list.html', {"groups" : groups, "gflag" : True})

@login_required(login_url='sign-in')
@user_passes_test(is_admin, login_url='no-parmission')
def view_group(request):
    groups = Group.objects.all()
    return render(request, 'admin/view_group.html', {"groups" : groups, "gflag" : True})

@login_required(login_url='sign-in')
@user_passes_test(is_admin, login_url='no-parmission')
def change_role(request, user_id):
    user = User.objects.get(id = user_id)
    
    form = AssignRoleForm()
    
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
        
            user.groups.clear() # remove old roles
            user.groups.add(role)
        
            return redirect('admin-dashboard')
    return render(request, 'admin/change_role.html', {"form" : form})

def check_user_id(user):
    return user.id 

@login_required(login_url='sign-in') 
@user_passes_test(is_participant, login_url='no-parmission')
def participant_dashboard(request, ):
    
    user_id = check_user_id(request.user)
    
    my_events = EventModel.objects.filter(participant = user_id)

    all_events = EventModel.objects.all()
    
    pflag = is_participant(request.user)
    context = {
        "all_events" : all_events,
        "my_events" : my_events,
        "pflag" : pflag,
    }
    return render(request, 'participant/participant_dashboard.html', context)


@login_required(login_url='sign-in')
@permission_required("events.view_participantmodel", login_url='no-parmission')
def all_participant(request):
    
    events = EventModel.objects.prefetch_related('participant').all()
    
        # count data
    count = all_count()
    
    context = {
        "events" : events,
        "count" : count,
    }
    
    
    return render(request, 'admin/all_participant.html', context)


@login_required(login_url='sign-in')
@permission_required("events.add_participantmodel", login_url='no-parmission')
def create_participant(request):
    participant_form = CustomRegistrationForm()
    
    if request.method == 'POST':
        participant_form = CustomRegistrationForm(request.POST)
        
        if participant_form.is_valid():
            participant_form.save()
            
            messages.success(request, "Participant added Successfully.")
            return redirect('create-participant')
    
    # count data
    count = all_count()
    
    context = {
        'participant_form' : participant_form,
        "count" : count
    }
    return render(request, 'admin/create_participant.html', context)


@login_required(login_url='sign-in')
@permission_required("events.change_participantmodel", login_url='no-parmission')
def update_participant(request, id):
    participant = get_object_or_404(User, id = id)
    
    participant_form = CustomUserUpdateForm(instance = participant)
    
    if request.method == 'POST':
        participant_form = CustomUserUpdateForm(request.POST, instance = participant)
        
        if participant_form.is_valid():
            participant_form.id = participant.id
            participant_form.save()
            messages.success(request, "Participant Updated Successfully.")
            return redirect('all-participant')
    
    count = all_count()
    
    context = {
        "participant" : participant,
        "participant_form" : participant_form,
        "count" : count,
    }
    return render(request, 'admin/update_participant.html', context)    

@login_required(login_url='sign-in')
@permission_required("events.delete_participantmodel", login_url='no-parmission')
def delete_participant(request, id):
    
    participant = User.objects.get(id = id)
    
    participant.delete()
    
    messages.success(request, "Participant Deleted Successfully .")
    return redirect('all-participant')


@login_required(login_url='sign-in')
def redirect_dashboard(request):
    
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_organizer(request.user):
        return redirect('manager-dashboard')
    elif is_participant(request.user):
        return redirect('participant-dashboard')
    return redirect('no-parmission')