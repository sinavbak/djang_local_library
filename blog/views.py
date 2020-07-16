from django.shortcuts import render

# Create your views here.
def index(request):
    data = {
        'current':"home",
    }
    return render(request,'blog/index.html',context = data)