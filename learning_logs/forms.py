from .views import Topic, Entry
from django import forms 

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = {'text'}
        labels = {'text' : ''}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = {'text'}
        labels = {'text' : ''}
        widgets = {'text' : forms.Textarea(attrs = {'cols' : 160})}