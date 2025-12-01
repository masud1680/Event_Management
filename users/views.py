from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from users.forms import CustomRegistrationForm, CustomLoginForm, CreateGroupForm,  GroupUpdateSelectForm, AssignRoleForm, CustomUserUpdateForm, EditProfileForm, PasswordChangeForm, PasswordResetForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import  Group
from django.contrib.auth.tokens import default_token_generator
from events.views import all_count, is_organizer, is_admin, is_participant
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from events.models import EventModel
import datetime

from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView, FormView, TemplateView, UpdateView
from django.core.exceptions import ImproperlyConfigured

from django.contrib.auth import get_user_model



User = get_user_model()

# Create your views here.
# def sign_up(request):
    
#     form = CustomRegistrationForm()
    
#     if request.method == 'POST':
#         form = CustomRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data.get('password'))
#             user.is_active = False
            
#             form.save()
#             messages.success(request, 'Registration Successful. \n\n A varification mail send on your email.')
#             return redirect('sign-in')
#         else:
#             messages.warning(request, "Registration Unsuccessfull!!")
    
#     return render(request, 'users_form/registration.html', {"form" : form})

class SignUpView(FormView):
    template_name = 'users_form/registration.html'
    form_class = CustomRegistrationForm
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get('password'))
        user.is_active = False
            
        form.save()
        messages.success(self.request, 'Registration Successful. \n\n A varification mail send on your email.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.warning(self.request, "Registration Unsuccessfull!!")
        response = super().form_invalid(form)
        return response
    
    
    
    
        
    
    


# def sign_in(request):
#     form = CustomLoginForm()
    
#     if request.method == 'POST':
#         form = CustomLoginForm(data = request.POST)
        
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             messages.success(request,'Login Successfull.')
#             return redirect('redirect-dashboard')
#     return render(request, 'users_form/login.html', {"form" : form})

class SignInView(LoginView):
    template_name = 'users_form/login.html'
    form_class = CustomLoginForm
    success_url = reverse_lazy('redirect-dashboard')

    def get_success_url(self):
        return self.success_url or self.get_default_redirect_url()


# @login_required(login_url='sign-in')
# def sign_out(request):
#     if request.method == 'POST':
#         logout(request)
        
#     return redirect('home')

class SignOut(LoginRequiredMixin, LogoutView):
    login_url = 'sign-in'
    
    def post(self, request, *args, **kwargs):
        logout(self.request)

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
    
# @user_passes_test(is_admin, login_url='no-parmission')
# def admin_dashboard(request):
#     users = User.objects.all()
    
#     aflag = is_admin(request.user)
    
#     count = all_count()
#     context ={
#         "users" : users,
#         "count" : count,
#         "aflag" : aflag,
#         }
    
#     return render(request, 'admin/dashboard.html', context) 
 
@method_decorator(user_passes_test(is_admin, login_url="no-permission"), name='dispatch')
class AdminDashboard(TemplateView):
    template_name = 'admin/dashboard.html'

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context["aflag"] = is_admin(self.request.user)
        context["count"] = all_count()
        context["users"] = User.objects.all()
        user = self.request.user
        print(user.username)
        context['profile_image'] = user.profile_image
        return context
    

# @login_required(login_url='sign-in')
# @user_passes_test(is_admin, login_url='no-parmission')
# def create_group(request):
#     form = CreateGroupForm()
    
#     if request.method == 'POST':
#         form = CreateGroupForm(request.POST)
#         group = form.save()
#         messages.success(request, f"{group.name} Role assign Successfull.")
#         return redirect('create-group')
    
#     return render(request, 'admin/create_group.html', {"form" : form, "gflag" : True})


@method_decorator(user_passes_test(is_admin, login_url="no-permission"), name='dispatch')
class CreateGroup(LoginRequiredMixin, CreateView):
    login_url = 'sign-in'
    template_name = 'admin/create_group.html'
    form_class = CreateGroupForm

    def post(self, request, *args, **kwargs):
        form = CreateGroupForm(request.POST)
        group = form.save()
        messages.success(request, f"{group.name} Role assign Successfull.")
        return redirect('create-group')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["gflag"] = True
        return context
    


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
    
    my_events = EventModel.objects.filter(Participant = user_id)

    all_events = EventModel.objects.all()
    
    pflag = is_participant(request.user)
    context = {
        "all_events" : all_events,
        "my_events" : my_events,
        "pflag" : pflag,
    }
    return render(request, 'participant/participant_dashboard.html', context)


# @login_required(login_url='sign-in')
# @permission_required("events.view_participantmodel", login_url='no-parmission')
# def all_participant(request):
    
#     events = EventModel.objects.prefetch_related('participant').all()
    
#         # count data
#     count = all_count()
    
#     context = {
#         "events" : events,
#         "count" : count,
#     }
    
    
#     return render(request, 'admin/all_participant.html', context)


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
@user_passes_test(is_organizer, login_url='no-parmission')
def organizer_dashboard(request):
    
    count = all_count()
   
    
    type = request.GET.get('type', 'all')
    
    date_now = datetime.date.today()
   

    # fatch all task
    base_query = EventModel.objects.all()
    
    if type == 'today':
        events = base_query.filter(date = date_now)
    elif type == 'upcoming':
        events = base_query.filter(date__gt = date_now)
    elif type == 'past':
        events = base_query.filter(date__lt = date_now)
    elif type == 'all':
        events = base_query.all()
    else:
        events = base_query.filter(date = date_now)
    
    # show all category in option
    
    EVcategories = EventModel.objects.select_related('category').all()
    oflag = is_organizer(request.user)
    aeflag = is_admin(request.user)
    
    context ={
        "count" : count,
        "events" : events,
        "EVcategories" : EVcategories,
        "oflag": oflag,
        "aeflag": aeflag,
    }
     
    return render(request,'organizer/organizer_dashboard.html', context)

@login_required(login_url='sign-in')
def redirect_dashboard(request):
    
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_organizer(request.user):
        return redirect('organizer-dashboard')
    elif is_participant(request.user):
        return redirect('participant-dashboard')
    return redirect('no-parmission')



# profile section working start

class ProfileView(TemplateView):
    template_name = 'profile/view_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['username'] = user.username
        context['name'] = user.get_full_name()
        context['email'] = user.email
        context['status'] = user.is_active
        context['gender'] = user.gender
        context['age'] = user.age
        context['profile_image'] = user.profile_image
        context['phone'] = user.phone
        context['blood_group'] = user.blood_group
        context['bio'] = user.bio
        context['description'] = user.description
        context['address'] = user.address
        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        return context




class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'profile/edit_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return redirect('view-profile')
    


class CustomePasswordChangeView(PasswordChangeView):
    template_name = 'registration/custome_password_change_form.html'
    success_url = reverse_lazy('view-profile')
    form_class = PasswordChangeForm

class CustomePasswordResetView(PasswordResetView):
    template_name = 'registration/custome_password_reset_form.html'
    form_class = PasswordResetForm

class CustomePasswordResetCompleteView(PasswordResetCompleteView):
             template_name = "registration/custome_password_reset_complete.html"

