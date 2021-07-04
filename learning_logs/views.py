from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic
from .models import Entry
from .forms import TopicForm, EntryForm

def index(request):
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    topics = Topic.objects.filter(owner = request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id = topic_id)
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic' : topic, 'entries' : entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    if request.method != 'POST':
        topic_form = TopicForm()
    else:
        topic_form = TopicForm(request.POST)
        if topic_form.is_valid():
            new_topic = topic_form.save(commit = False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'topic_form' : topic_form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id = topic_id)
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        entry_form = EntryForm()
    else:
        entry_form = EntryForm(request.POST)
        new_entry = entry_form.save(commit = False)
        new_entry.topic = topic
        new_entry.save()
        return HttpResponseRedirect(reverse('learning_logs:topic', args = [topic_id]))
    context = {'topic' : topic, 'entry_form' : entry_form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id = entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        entry_form = EntryForm(instance = entry)
    else:
        entry_form = EntryForm(instance = entry, data = request.POST)
        if entry_form.is_valid():
            entry_form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args = [topic.id]))
    context = {'topic' : topic, 'entry_form' : entry_form, 'entry' : entry}
    return render(request, 'learning_logs/edit_entry.html', context)


