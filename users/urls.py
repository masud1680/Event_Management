from django.urls import path
from users.views import sign_up, sign_in, sign_out, active_account,admin_dashboard, create_group, view_group,view_group_update_list, update_group_data, change_role, participant_dashboard, create_participant, update_participant, delete_participant, redirect_dashboard
from django.contrib.auth import views as auth_views
urlpatterns = [
    
    path('sign-up/', sign_up, name='sign-up'),
    path('sign-in/', sign_in, name='sign-in'),
    path('sign-out/', sign_out, name='sign-out'),
    path('activate/<int:user_id>/<str:token>/', active_account , ),
    path("password-reset/", 
         auth_views.PasswordResetView.as_view(
             template_name="registration/password_reset_form.html"
             
             ), 
         name="password_reset"),

    path("password-reset/done/", 
         auth_views.PasswordResetDoneView.as_view(), 
         name="password_reset_done"),

    path("reset/<uidb64>/<token>/", 
         auth_views.PasswordResetConfirmView.as_view(), 
         name="password_reset_confirm"),

    path("reset/done/", 
         auth_views.PasswordResetCompleteView.as_view(), 
         name="password_reset_complete"),
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('redirect-dashboard/', redirect_dashboard, name='redirect-dashboard'),
    path('create-group/', create_group, name='create-group'),
    path('view/group/', view_group, name='view-group'),
    path('update/group/', view_group_update_list, name='update-group'),
    path('update/<int:group_id>/group/', update_group_data, name='update-group-data'),
    path('change-role/<int:user_id>/', change_role, name='change-role'),
    path('participant/dashboard/', participant_dashboard, name='participant-dashboard'),
    path('create-participant/', create_participant, name='create-participant'),
    path('update-participant/<int:id>', update_participant, name='update-participant'),
    path('delete-participant/<int:id>', delete_participant, name='delete-participant'),
]