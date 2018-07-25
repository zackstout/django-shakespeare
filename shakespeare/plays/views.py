
from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import PlayName, PlayText, Comment
import requests, datetime, time, re

# Create your views here.
def index(request, id):
    p = PlayName.objects.all()[:20]
    text = PlayText.objects.filter(play_id=id).order_by('act', 'scene', 'lineno')
    prevSpeaker = 'ahhhh'

    clipped = text[4:200]

    # Just grabbing first 200 lines for now, because counting is costly:
    for t in clipped:
        # Get rid of leading and trailing quote marks:
        t.text = re.sub('^"', '', t.text)
        t.text = re.sub('"$', '', t.text)
        t.showSpeaker = True

        # Only show speaker name if they are a new speaker:
        if t.speaker == prevSpeaker:
            t.showSpeaker = False
        prevSpeaker = t.speaker

        # Get number comments (NOTE that this seems quite costly):
        t.num_comments = Comment.objects.filter(line_id=t.id).count()

    title = PlayName.objects.filter(id=id)[0].asString()
    title = re.sub('(?P<char>[A-Z\d])', ' \g<1>', title)
    title = re.sub(',', ', ', title)
    # Still imperfect, missing "part", "of", "and", inappropriately splitting "V I"

    context = {
        'text': clipped,
        'title': title.strip(),
        # 'play_id': id
    }

    return render(request, 'plays/play.html', context)


def comment(request, id):
    play_id = PlayText.objects.filter(id=id)[0].play_id

    if request.method == "GET":
        text = PlayText.objects.filter(id=id)[0].text
        context = {
            'id': id,
            'text': text,
            'play_id': play_id
            }
        return render(request, 'comments/comment.html', context)
    elif request.method == "POST":
        commentInput = request.POST['commentInput']
        line_id = PlayText.objects.filter(id=id)[0]
        comment = Comment(text=commentInput, line_id=line_id)
        comment.save()

        return HttpResponseRedirect(reverse('index', args=(play_id,)))
