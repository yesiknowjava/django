import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import LEAVE_TYPE
from .models import LEAVE_STATUS
from .models import *
# Create your views here.

def user_login(request):
    if request.user.is_authenticated:
        return redirect('/employeedashboard')
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == '' or password == '':
            messages.warning(request, 'Username or Password empty')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            employee = Employee.objects.get(id=user.id)
            if employee.manager:                
                return redirect('managerdashboard/')
            else:
                return redirect('employeedashboard/')
        else:
            messages.warning(request, 'Invalid Username, Password entered.')
        return render(request, 'index.html', context=context)
    return render(request, 'index.html', context=context)

def user_logout(request):
    logout(request)
    return redirect('/')

@login_required
def employeedashboard(request):
    employee = Employee.objects.get(id=request.user.id)
    context = {'employee': employee}
    leaves = Leave.objects.filter(requester = request.user.id)
    context.update({'leaves': leaves})
    return render(request, 'employeedashboard.html', context=context)

@login_required
def applyleave(request):
    context = {'leave_type': LEAVE_TYPE}
    if request.method == 'POST':
        leave_type = request.POST.get('leave_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')

        if leave_type == '' or start_date == '' or end_date == '' or reason == '':
            messages.warning(request, 'All fields are mandatory')
            return redirect('applyleave')
        else:
            manager = Employee.objects.filter(manager = True).first()
            requester = Employee.objects.get(id=request.user.id)
            leave = Leave()
            leave.requester = requester
            leave.approver = manager
            leave.reason = reason
            leave.leave_type = leave_type
            print(start_date)
            print(end_date)
            leave.start_date = datetime.datetime.strptime(start_date, "%m/%d/%Y")
            leave.end_date = datetime.datetime.strptime(end_date, "%m/%d/%Y")
            messages.success(request, 'Your leave has been applied successfully')
            leave.save()
            return redirect('employeedashboard')
    return render(request, 'employee_applyleave.html', context=context)

@login_required
def deleteleave(request, leave_id=None):
    user = Employee.objects.get(id=request.user.id)
    leave = Leave.objects.get(id=leave_id)
    if user.manager:
        leave.delete()
        return redirect('managerdashboard')
    else:
        if leave.leave_status <= 1:
            messages.success(request, 'Leave deleted successfully')
            leave.delete()
        else:
            messages.warning(request, 'Your current leave is being viewed by the manager. You cannot delete the same')
        return redirect('employeedashboard')


@login_required
def managerdashboard(request):
    employee = Employee.objects.get(id=request.user.id)
    context = {'employee': employee}
    leaves_pending = Leave.objects.filter(leave_status = 1)
    leaves_approved = Leave.objects.filter(leave_status = 2)
    leaves_rejected = Leave.objects.filter(leave_status = 3)
    context.update({'leaves_pending': leaves_pending, 'leaves_approved': leaves_approved, 'leaves_rejected': leaves_rejected})
    return render(request, 'managerdashboard.html', context=context)

@login_required
def approveleave(request, leave_id=None):
    user = Employee.objects.get(id=request.user.id)
    leave = Leave.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    context = {}
    messages.warning(request, 'Leave has been approved')
    return redirect('managerdashboard')


@login_required
def rejectleave(request, leave_id=None):
    user = Employee.objects.get(id=request.user.id)
    leave = Leave.objects.get(id=leave_id)
    leave.leave_status = 3
    leave.save()
    context = {}
    messages.warning(request, 'Leave has been rejected')
    return redirect('managerdashboard')