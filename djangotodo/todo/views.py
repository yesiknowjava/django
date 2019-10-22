from django.shortcuts import render, redirect
from django.contrib import messages
# from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import List
from .forms import ListForm
# Create your views here.
def home(request):
    all_items = List.objects.all()
    context = {'all_items': all_items}
    if request.method == "POST":
        form = ListForm(request.POST or None)
        if form.is_valid:
            form.save()
            messages.success(request, ('Task added successfully'))
            return redirect(reverse('home'))
        else:
            messages.error(request, ('There was an error in the form'))
            return redirect(reverse('home'))
        
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html', {})

def edit(request, list_id):
    try:
        item = List.objects.get(id=list_id)
        if request.method == "POST":
            form = ListForm(request.POST or None, instance=item)
            if form.is_valid:
                form.save()
                messages.success(request, ('Task edited successfully'))
                return redirect(reverse(home))
            else:
                messages.error(request, ('There were some issues in the task'))
                return redirect(reverse(edit,args=[list_id]))
        else:
            print('this was here', item.id)           
            return render(request, 'edit.html', {'item': item})
    except Exception as e:
        print(str(e))
        messages.error(request, ('Item not found'))
        return redirect(reverse(home))
    
    

def delete(request, list_id):
    try:
        item = List.objects.get(id=list_id)
        item.delete()
        messages.success(request, ('Item deleted successfully'))
    except:
        messages.error(request, ('Item not found'))
    return redirect(reverse(home))
    
def cross(request, list_id):
    try:
        item = List.objects.get(id=list_id)
        if item.completed:
            messages.error(request, ('Item not completed'))
            item.completed = False
        else:
            messages.warning(request, ('Item completed successfully'))
            item.completed = True
        item.save()
    except:
        messages.error(request, ('Item not found'))
    return redirect(reverse(home))
