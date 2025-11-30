# Convarted 5 views are => SignUpView, SignInView, SignOut, AdminDashboard, CreateGroup, 

from django.urls import path
# from users.views import sign_up, sign_in, sign_out, active_account,admin_dashboard, create_group, view_group,view_group_update_list, update_group_data, change_role, participant_dashboard, create_participant, update_participant, delete_participant, redirect_dashboard, organizer_dashboard 
from users.views import SignUpView, SignInView, SignOut, ProfileView, EditProfileView, CustomePasswordChangeView, CustomePasswordResetView, active_account, AdminDashboard, CreateGroup, view_group,view_group_update_list, update_group_data, change_role, participant_dashboard, create_participant, update_participant, delete_participant, redirect_dashboard, organizer_dashboard 
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeDoneView
urlpatterns = [
    
#     path('sign-up/', sign_up, name='sign-up'),
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
#     path('sign-in/', sign_in, name='sign-in'),
    path('sign-in/', SignInView.as_view(), name='sign-in'),
#     path('sign-out/', sign_out, name='sign-out'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('activate/<int:user_id>/<str:token>/', active_account , ),
    path("password-reset/", CustomePasswordResetView.as_view(  ), name="reset-password"),

    path("password-reset/done/", CustomePasswordResetView.as_view(template_name = 'registration/custome_password_reset_done.html'),  name="password_reset_done"),

    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),

    path("reset/done/", 
         auth_views.PasswordResetCompleteView.as_view(), 
         name="password_reset_complete"),
#     path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/dashboard/', AdminDashboard.as_view(), name='admin-dashboard'),
    path('redirect-dashboard/', redirect_dashboard, name='redirect-dashboard'),
#     path('create-group/', create_group, name='create-group'),
    path('create-group/', CreateGroup.as_view(), name='create-group'),
    path('view/group/', view_group, name='view-group'),
    path('update/group/', view_group_update_list, name='update-group'),
    path('update/<int:group_id>/group/', update_group_data, name='update-group-data'),
    path('change-role/<int:user_id>/', change_role, name='change-role'),
    path('participant/dashboard/', participant_dashboard, name='participant-dashboard'),
    path('organizer/dashboard/', organizer_dashboard, name='organizer-dashboard'),
    path('create-participant/', create_participant, name='create-participant'),
    path('update-participant/<int:id>', update_participant, name='update-participant'),
    path('delete-participant/<int:id>', delete_participant, name='delete-participant'),


    path('profile/', ProfileView.as_view(), name="view-profile"),
    path('edit-profile/', EditProfileView.as_view(), name="edit-profile"),
    path('change-password/', CustomePasswordChangeView.as_view(), name="change-password"),
]