from django.urls import path
from . import views


urlpatterns = [
    path('', views.manager_dashboard, name='manager-dashboard'),
    path('create-event/', views.create_event,  name="create-event"),
    path('create-participant/', views.create_participant, name='create-participant'),
    path('update-participant/<int:id>', views.update_participant, name='update-participant'),
    path('delete-participant/<int:id>', views.delete_participant, name='delete-participant'),
    path('update-event/<int:id>', views.update_event, name='update-event'),
    path('delete-event/<int:id>', views.delete_event, name='delete-event'),
    path('event-details/<int:id>', views.view_event_details , name='event-details'),
    path('all-participant/', views.all_participant , name='all-participant'),
    path('view-event-category/<int:id>', views.view_event_category , name='view-event-category'),
    path('search-results/', views.search_text , name='search-results'),
    path('search-with-category/', views.search_with_category, name='search-with-category'),
    path('search-with-date-range/', views.search_with_date_range, name='search-with-date-range'),
    path('site-maintenance/', views.site_maintenance, name='site-maintenance'),
]