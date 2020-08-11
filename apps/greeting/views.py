from django.shortcuts import render


def index(request):
    context = {
        'greeting': 'Greeting',
    }
    return render(request, 'greeting/greeting.html', context)
