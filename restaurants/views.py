from django.shortcuts import render
#from django.contrib.auth.decorators import login_required

# Create your views here.
from django.shortcuts import render
def index(request):

    return render(request, "index.html")