from django.shortcuts import render

from .models import Tool

def index(request):
    context = {
        'segment': 'index',
        'tools': Tool.objects.all(),
        'best': Tool.objects.all().order_by('-rating').first(),
        'newest': Tool.objects.order_by('-created').first(),
    }
    return render(request, 'home/index.html', context)

def tool(request, tool):
    return render(request, 'home/tool.html', {'segment': 'index', 'tool': tool})

def add(request):
    return render(request, 'home/add.html', {'segment': 'add'})

