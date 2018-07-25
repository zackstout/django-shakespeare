
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import PlayName, PlayText
import requests, datetime, time

# Create your views here.
def index(request, id):
    p = PlayName.objects.all()[:20]
    text = PlayText.objects.filter(play_id=id).order_by('act', 'scene', 'lineno')

    # return HttpResponse(text)
    context = {'text': text}
    return render(request, 'plays/play.html', context)
