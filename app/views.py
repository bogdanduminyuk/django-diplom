from django.shortcuts import render


def index(request):
    return render(request, 'app/index.html', {'title': 'my_title'})
