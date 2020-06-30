from django.shortcuts import render


# Create your views here.

def index(request):
    context = {
        'page_title': "Home"
    }
    return render(request, 'MyPage/index.html', context)
