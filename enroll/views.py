from pyexpat.errors import messages
from django.shortcuts import redirect, render
from .forms import StudentRegistration
from .models import User


# This function will add new item and show new items
def add(request):
    if request.method == 'POST':
        form = StudentRegistration(request.POST)
        if form.is_valid():
            title = request.POST['title']
            description = request.POST['description']
            reg = User(title=title, description=description)
            reg.save()
        return redirect(show)
    else:
        form = StudentRegistration()
    return render(request, 'enroll/add.html', {'form': form})


def show(request):
    show = User.objects.all()
    return render(request, 'enroll/show.html', {'show': show})


# This Function will update/Edit
def update_data(request, id):
    if request.method == 'POST':
        pi = User.objects.get(pk=id)
        form = StudentRegistration(request.POST, instance=pi)
        if form.is_valid():
            form.save()
    else:
        pi = User.objects.get(pk=id)
        form = StudentRegistration(instance=pi)
    return render(request, 'enroll/updatestudent.html', {'form': form})


def delete_data(request, id):
    if request.method == 'POST':
        pi = User.objects.get(pk=id)
        pi.delete()
        return redirect(show)
        # return render(request, 'enroll/show.html')


def dashboard(request):
    return render(request, "enroll/dashboard.html")
