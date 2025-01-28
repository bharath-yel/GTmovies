from django.shortcuts import render

def index(request):
    template_data = {}
    template_data['title'] = 'GTmovies'
    #render is used to render templates and return an HTTP response
    return render(request, 'home/index.html', {
        'template_data' : template_data})

def about(request):
    return render(request, 'home/about.html')