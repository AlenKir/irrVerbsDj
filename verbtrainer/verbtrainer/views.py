from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    if request.method == 'POST':
        level = request.POST.get('level')
        request.session['level'] = level
        return redirect(reverse('index'))
    level = request.session.get('level')
    return render(request, 'verbtrainer/index.html',
                  {'level': level})
