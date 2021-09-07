from django.shortcuts import render, redirect

def home(request):
    # context = {
    #     'yooooo': 12345,
    # }

    return render(request, 'home.html')
