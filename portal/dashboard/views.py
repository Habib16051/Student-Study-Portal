from django.shortcuts import render, redirect
from django.contrib import messages
from . forms import *
from django.views import generic
from youtubesearchpython import VideosSearch
# Create your views here.


def home(request):
    return render(request, 'dashboard/home.html')


def notes(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            notes = Note(
                user=request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()

        messages.success(
            request, f"Notes Added from {request.user.username} Successfully!")

    else:
        form = NoteForm()
    notes = Note.objects.filter(user=request.user)
    context = {'notes': notes, 'form': form}
    return render(request, 'dashboard/notes.html', context)


def delete_note(request, pk=None):
    Note.objects.get(id=pk).delete()
    return redirect("notes")


class NoteDetailView(generic.DetailView):
    model = Note


def homework(request):
    
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
                    
            except:
                finished = False
                
            work = Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished
                
            )
            work.save()
            messages.success(request, f'Homework added from {request.user.username}!!')
                
    form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        work_done = True
    else:
        work_done = False
    context = {'homework': homework, 'work_done':work_done, 'form':form}
    return render(request, 'dashboard/homework.html', context)


def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
        
    homework.save()
    return redirect('homework')

def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')
    
def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=100)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input':text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
                    
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form':form,
                'results': result_list
            }
        
        return render(request, 'dashboard/youtube.html', context) 
        
    else:
    
        form = DashboardForm()
    context = {'form':form}
    return render(request, 'dashboard/youtube.html', context)
    
    
def todo(request):
    return render(request, 'dashboard/todo.html')