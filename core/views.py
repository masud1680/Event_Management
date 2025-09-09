from django.shortcuts import render

# Create your views here.

def home(request):
    
    return render(request, 'home.html')

def site_maintenance(request):
    
    return render(request, 'site_maintenance.html')

def no_parmission(request):
    return render(request, 'no_parmission.html')
