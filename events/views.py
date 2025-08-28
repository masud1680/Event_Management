from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from events.models import EventModel, ParticipantModel, CategoryModel
from events.forms import EventForm, EventModelForm, participentModelForm, categoryModelForm
from datetime import date, time
from django.db.models import Q, Count, Max, Min, Avg
import datetime
from django.contrib import messages


# Create your views here.


def all_count():
    date_now = datetime.date.today()
    counts = EventModel.objects.aggregate(
        
        # total_participant = Count('assignet_to.id'),
        total_event = Count('id', distinct=True),
        today_event = Count("id", filter=Q(date = date_now), distinct=True),
        upcoming_event = Count("id", filter=Q(date__gt = date_now), distinct=True),
        past_event = Count("id", filter=Q(date__lt = date_now), distinct=True),
        total_participant = Count("assigned_to", distinct=True),
        
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
       
    
    context ={
        "count" : count,
        "events" : events,
        "EVcategories" : EVcategories,
    }
     
    return render(request,'manager_dashboard.html', context)



def create_event(request):
    
    
    
    if request.method == 'POST':
        event_form = EventModelForm(request.POST)
        category_form = categoryModelForm(request.POST)
        
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
        event_form = EventModelForm(request.POST, instance = event)
        category_form = categoryModelForm(request.POST, instance = event.category)
        
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
        
def create_participant(request):
    participant_form = participentModelForm()
    
    if request.method == 'POST':
        participant_form = participentModelForm(request.POST)
        
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
    return render(request, 'create_participant.html', context)

def update_participant(request, id):
    participant = get_object_or_404(ParticipantModel, id = id)
    
    participant_form = participentModelForm(instance = participant)
    
    if request.method == 'POST':
        participant_form = participentModelForm(request.POST, instance = participant)
        
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
    return render(request, 'update_participant.html', context)    

def delete_participant(request, id):
    
    participant = ParticipantModel.objects.get(id = id)
    
    participant.delete()
    
    messages.success(request, "Participant Deleted Successfully .")
    return redirect('all-participant')

def view_event_details(request, id):
    # Fetch the event and prefetch participants
    events = EventModel.objects.prefetch_related("assigned_to").get(id=id)

    # for participant in events.assigned_to.all():
    #     print(participant.name)
    
    # count data
    count = all_count()
    
    context ={
        "events" : events,
        "count" : count
    }
    return render(request, 'event_details.html', context)


def all_participant(request):
    
    events = EventModel.objects.prefetch_related('assigned_to').all()
    
        # count data
    count = all_count()
    
    context = {
        "events" : events,
        "count" : count
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
            
    
    # print(all_category)
    # for cat in all_category.category.all():
    #     print(cat)
    
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
            
            

def site_maintenance(request):
    
    return render(request, 'site_maintenance.html')