
from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import PlayName, PlayText, Comment
import requests, datetime, time, re

# Create your views here.

ignores = ['.', ',', ':', ';', '-', '?', '!']

def handleClipped(clipped):
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
        t.words_clean = []

        for w in t.words:
            word = ''
            for c in w:
                if c not in ignores:
                    word = word + c
            t.words_clean.append(word)

# Adding info about each word (for now, other times in the play the word is used):
def getWordContexts(word, play_id):
    word_info = []
    if word != '':
        lines = PlayText.objects.all().filter(play_id=play_id)
        for l in lines:
            if word in l.text:
                info = {
                    'text': l.text,
                    'lineno': l.lineno,
                    'scene': l.scene,
                    'act': l.act,
                    'speaker': l.speaker
                }
                word_info.append(info)
    return word_info


def handleTitle(title):
    # Still imperfect, missing "part", "of", "and", inappropriately splitting "V I":
    title = re.sub('(?P<char>[A-Z\d])', ' \g<1>', title)
    title = re.sub(',', ', ', title)
    return title.strip()


def index(request, id, act=0, scene=0, word=''):
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

    handleClipped(clipped)

    context = {
        'text': clipped,
        'title': handleTitle(PlayName.objects.filter(id=id)[0].asString()),
        'play_id': id,
        # Yikes:
        'word': word,
        'word_info': getWordContexts(word, id),
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
            }
        return render(request, 'comments/comment.html', context)

    elif request.method == "POST":
        commentInput = request.POST['commentInput']
        line_id = PlayText.objects.filter(id=id)[0]
        comment = Comment(text=commentInput, line_id=line_id)
        comment.save()
        return HttpResponseRedirect(reverse('index', args=(play_id,)))


def comments(request, id):
    comments = Comment.objects.filter(line_id=id)
    context = {
        'comments': comments
    }
    return render(request, 'comments/comments.html', context)
