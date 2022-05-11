from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import StudentRegistration
from .models import User
from django.contrib import messages

#This function will add new item and show new items
def add(request):
    if request.method == 'POST':
        form= StudentRegistration(request.POST)
        if form.is_valid():
            title = request.POST['title']
            description = request.POST['description']
            reg = User(title=title, description=description)
            reg.save()
            form= StudentRegistration()
    else:
         form= StudentRegistration()
    return render(request, 'enroll/add.html',{ 'form':form })
    


def show(request):
    show = User.objects.all()
    return render(request, 'enroll/show.html', {'show': show})


#This Function will update/Edit
def update_data(request, id):
    if request.method == 'POST':
        pi = User.objects.get(pk=id)
        form = StudentRegistration(request.POST, instance=pi)
        if form.is_valid():
         form.save()
    else:
         pi = User.objects.get(pk=id)
         form = StudentRegistration( instance=pi)
    return render(request, 'enroll/updatestudent.html', {'form':form})


def complete_task(request, id):
    User = User.objects.get(pk=id)
    if User.users == request.user:

        User.is_active = True
        User.save()
    else:
        messages.error(request, ("Access Restricted! You Are Not Allowed!"))
    return redirect('add_show')


def pending_task(request, id):
    User = User.objects.get(pk=id)
    User.is_active = False
    User.save()
    return redirect('add_show')
            


#this function will delete data
def delete_data(request, id):
    if request.method == 'POST':
        pi=User.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/')

def dashboard(request):
    return render(request, "enroll/dashboard.html")

