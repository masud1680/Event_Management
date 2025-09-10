from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from events.models import EventModel,  CategoryModel
from events.forms import  EventModelForm,  categoryModelForm
from datetime import date, time
from django.db.models import Q, Count, Max, Min, Avg
import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail


def is_organizer(user):
    return user.groups.filter(name="Organizer").exists()

def is_admin(user):
    return user.groups.filter(name="Admin").exists()

# Create your views here.


def all_count():
    date_now = datetime.date.today()
    counts = EventModel.objects.aggregate(
        
        
        total_event = Count('id', distinct=True),
        today_event = Count("id", filter=Q(date = date_now), distinct=True),
        upcoming_event = Count("id", filter=Q(date__gt = date_now), distinct=True),
        past_event = Count("id", filter=Q(date__lt = date_now), distinct=True),
        total_participant = Count("Participant", distinct=True),
        
    )
    
    count = {"event" : counts['total_event'],"today" : counts['today_event'],"upcoming" : counts['upcoming_event'],"past" : counts['past_event'],"participants" : counts['total_participant'] }
    return count

def manager_dashboard(request):
    
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
     
    return render(request,'manager/manager_dashboard.html', context)



def create_event(request):
    
    
    
    if request.method == 'POST':
        event_form = EventModelForm(request.POST, request.FILES,)
        category_form = categoryModelForm(request.POST, request.FILES,)
        
        if event_form.is_valid() and category_form.is_valid():
            """Form to Model to database save"""
            category = category_form.save()
            events = event_form.save(commit=False)
            
            events.category = category
            events.save()
            event_form.save_m2m()
            
            messages.success(request, "Event Added Successfully.")
            return redirect('create-event')
    
    # count data
    count = all_count()
    

    
    event_form = EventModelForm()
    category_form = categoryModelForm()
    
    
    context = {
        "event_form" : event_form,
        "category_form" : category_form,
         "count" : count,
        
    }
    
    return render(request, 'event_form.html', context)
            
def update_event(request, id):
    event = get_object_or_404(EventModel,id = id)
    
    
    if request.method == 'POST':
        event_form = EventModelForm(request.POST, request.FILES, instance = event)
        category_form = categoryModelForm(request.POST, request.FILES, instance = event.category)
        
        if event_form.is_valid() and category_form.is_valid():
            category = category_form.save()
            events = event_form.save(commit=False)
            events.category = category
            events.id = event.id
            events.save()
            event_form.save_m2m()
            
            
            messages.success(request, "Event Updated Successfully.")
            return redirect('event-details', id)
    
        # count data
    count = all_count()
    
    # Pre-fill forms with existing data
    event_form = EventModelForm(instance=event) 
    if event.category:
        category_form = categoryModelForm(instance = event.category)  
              
    context = {
        "event_form" : event_form,
        "category_form" : category_form,
        "event" : event,
        "count" : count,
        
    }
    
    return render(request, 'event_update_form.html' , context)

def delete_event(request, id):
    if request.method == 'POST':
        event = EventModel.objects.get(id = id)
        event.delete()
        messages.success(request, "Event Deleted Successfully.")
        
    else:
        messages.success(request, "Something went wrong.")
    
    return redirect('manager-dashboard')

def view_event_details(request, id):
    # Fetch the event and prefetch participants
    events = EventModel.objects.prefetch_related("Participant").get(id=id)


    # count data
    count = all_count()
    
    context ={
        "events" : events,
        "count" : count
    }
    return render(request, 'event_details.html', context)


def all_participant(request):
    
    events = EventModel.objects.prefetch_related('Participant').all()
    # participants = User.objects.prefetch_related('eventP').all()
    
    participant_list = []
    
    for event in events:
        for par in event.Participant.all():
            if par not in participant_list:
                participant_list.append(par)
            
            
    
        # count data
    count = all_count()
    
    context = {
        "events" : events,
        "participant_list" : participant_list,
        "count" : count,
    }
    
    return render(request, 'all_participant.html', context)

def view_event_category(request, id):
    events = EventModel.objects.select_related("category").get(id = id)
    
        # count data
    count = all_count()
    
    context ={
        "events" : events,
        "count" : count
    }
    return render(request, 'event_category.html', context)


def search_text(request):
    
    if request.method == 'POST':
        query = request.POST['search']
        # print(query)
        
        if len(query) > 100:
            all_event = EventModel.objects.none()
        else:
            event_title = EventModel.objects.filter(title__icontains = query)
            event_location = EventModel.objects.filter(location__icontains = query)
           
            
            all_event = event_title.union(event_location)
               
    if all_event.count() == 0:
        messages.warning(request, "No Search Results.......  ")
    
    # count data
    count = all_count()
    
    # print(all_event.count())    
    context ={
        
        "query" : query,
        "all_event" : all_event,
        "count" : count
    }
    
    return render(request, 'search_box.html', context )


def search_with_category(request):
    if request.method == 'POST':
        id = request.POST.get('id')

        if id:
            all_event = EventModel.objects.filter(category_id=id)
            
            messages.success(request, "Here is your  Category Evant's.....")
            
        else:
            messages.warning(request, "No Category Evant's founds....")
            
    
    # count data
    count = all_count()
    
    context = {
        "all_event" : all_event,
        "count" : count
    }
    
    return render(request, 'search_box.html', context )

def search_with_date_range(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        if start_date and end_date:
            all_event = EventModel.objects.filter(date__range=[start_date, end_date])

            if all_event.count() == 0:
                messages.warning(request, "No Events Found.....")
            else:
                messages.success(request, "Here is your  Event's.....")
                
    # count data
    count = all_count()
    
    context= {
        "all_event" : all_event,
        "count" : count
    }
    return render(request, 'search_box.html', context)
            
            
def register_event(request, user_id, event_id):
    
    user = User.objects.get(id = user_id)
    registered_events = user.eventP.all()
    
    flag = False
    
    for revent in registered_events:
        if revent.id == event_id:
            flag = True
            
        
    if flag == True:    
        messages.warning(request, "Event  already registered.")
    else:
        event = EventModel.objects.get(id = event_id)
        event.Participant.add(user)
        messages.success(request, "Event  added Successfull.")
        send_rEmail(user, event)      
    return redirect('redirect-dashboard')

# send_email_when_register_evant

def send_rEmail(user,event):
        subject = "Evant Registration."
        message = f"Hi, {user.first_name} {user.last_name}. \n\n You are registered  : \n {event.title} event successfull. \n\n Thank You."
        recipient_list = [user.email]
        
        
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        except Exception as e:
            print(f"Failed to send {user.email} : {str(e)}")    
    