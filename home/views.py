from django.shortcuts import render

def index(request):
    #render is used to render templates and return an HTTP response
    return render(request, 'home/index.html')

def about(request):
    return render(request, 'home/about.html')