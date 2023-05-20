from django.shortcuts import render
from . forms import *

# Create your views here.
def home(request):
    return render(request, 'dashboard/home.html')

def notes(request):
    form = NoteForm()
    notes = Note.objects.filter(user=request.user)
    context = {'notes': notes, 'form':form}
    return render(request, 'dashboard/notes.html', context)