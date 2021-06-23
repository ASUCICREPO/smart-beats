from django.shortcuts import render


def index(request):
    context = {'test': 'test'}
    return render(request, 'beats/index.html')
