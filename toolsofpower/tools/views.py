from django.shortcuts import render

from .models import Tool

def index(request):
    context = {
        'segment': 'index',
        'tools': Tool.objects.all(),
        'best': Tool.objects.all().order_by('-rating').first(),
        'newest': Tool.objects.latest('created'),
    }
    return render(request, 'home/index.html', context)

def add(request):
    return render(request, 'home/add.html', {'segment': 'add'})

def parser(request):
    return render(request, 'home/parser.html', {'segment': 'parser'})
