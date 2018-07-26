
from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import PlayName, PlayText, Comment
import requests, datetime, time, re

# Create your views here.

def index(request, id, act=0, scene=0, word=''):
    wordInfo = False
    # Odd way of doing this, since we're passing these in as params....
    if request.method == "POST":
        act = request.POST['act']
        scene = request.POST['scene']
        print(act, scene)

    # User might be asking for whole play, or one scene:
    if act==0:
        text = PlayText.objects.filter(play_id=id).order_by('act', 'scene', 'lineno')
        clipped = text[4:200]
    else:
        text = PlayText.objects.filter(play_id=id,act=act,scene=scene).order_by('act', 'scene', 'lineno')
        clipped = text

    prevSpeaker = ''

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

        # Split the line into words for NLTK analysis:
        t.words = t.text.split()

    # Still imperfect, missing "part", "of", "and", inappropriately splitting "V I":
    title = PlayName.objects.filter(id=id)[0].asString()
    title = re.sub('(?P<char>[A-Z\d])', ' \g<1>', title)
    title = re.sub(',', ', ', title)

    word_info = []

    if word != '':
        wordInfo = True
        lines = PlayText.objects.all()
        print("text is: " + lines[10].text)
        for l in lines:
            if word in l.text:
                word_info.append(l.text)

        # lines = PlayText.objects.filter(play_id=id)

    context = {
        'text': clipped,
        'title': title.strip(),
        'play_id': id,
        # Yikes:
        'wordInfo': wordInfo,
        'word': word,
        'word_info': word_info,
    }

    return render(request, 'plays/play.html', context)


def comment(request, id):
    play_id = PlayText.objects.filter(id=id)[0].play_id

    if request.method == "GET":
        text = PlayText.objects.filter(id=id)[0].text
        context = {
            'id': id,
            'text': text,
            'play_id': play_id,
            # 'wordInfo': False
            }
        return render(request, 'comments/comment.html', context)
    elif request.method == "POST":
        commentInput = request.POST['commentInput']
        line_id = PlayText.objects.filter(id=id)[0]
        comment = Comment(text=commentInput, line_id=line_id)
        comment.save()

        return HttpResponseRedirect(reverse('index', args=(play_id,)))
