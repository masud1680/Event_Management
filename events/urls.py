from django.urls import path
from . import views


urlpatterns = [
    path('', views.events_dashboard, name='events-dashboard'),
    path('create-event/', views.create_event,  name="create-event"),
    path('update-event/<int:id>', views.update_event, name='update-event'),
    path('delete-event/<int:id>', views.delete_event, name='delete-event'),
    path('event-details/<int:id>', views.view_event_details , name='event-details'),
    path('register-event/<int:user_id>/<int:event_id>/', views.register_event , name='register-event'),
    path('all-participant/', views.all_participant , name='all-participant'),
    path('view-event-category/<int:id>', views.view_event_category , name='view-event-category'),
    path('search-results/', views.search_text , name='search-results'),
    path('search-with-category/', views.search_with_category, name='search-with-category'),
    path('search-with-date-range/', views.search_with_date_range, name='search-with-date-range'),
 
]