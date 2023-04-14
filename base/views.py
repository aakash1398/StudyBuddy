from django.shortcuts import render,redirect
from .models import Room, Topic, Message
from django.contrib.auth.models import User
from .forms import Roomform
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.


# rooms = [
#     {'id' : 1, 'name' : 'Python Learning Beginners'},
#     {'id' : 2, 'name' : 'Django web development'},
#     {'id' : 3, 'name' : 'SQL advanced topics'},
# ]


def home(request):

    q = request.GET.get('q') if request.GET.get('q')!=None else '';

    topics = Topic.objects.all()

    rooms = Room.objects.filter(Q(topic__name__icontains=q)| Q(name__icontains=q)| Q(description__icontains=q) |Q(host__username__icontains=q)) # blank '' return all records

    context = {'rooms': rooms, 'topics' : topics}
    return render(request,'base/home.html', context)


def room(request,pk):

    

    try:
        room_name = Room.objects.get(id=pk)

        room_message = room_name.message_set.all().order_by('created') # give us the set of messages related to this specific room

        participants = room_name.participants.all()


        if request.method == 'POST':
            user_message = Message.objects.create(
                user = request.user,
                room = room_name,
                body = request.POST.get('body')
            )
            room_name.participants.add(user_message.user)
            return redirect('room', pk=room_name.id)
    except:
        raise ValueError('no such room found')

    context = {'room_data': room_name, 'room_message': room_message, 'participants': participants}

    return render(request,'base/room.html', context)
  
@login_required(login_url='login')
def create_room(request):
    form = Roomform()

    if request.method == 'POST':
        form  = Roomform(request.POST)
        if form.is_valid:
            form.save()
            return redirect('home')


    context = {'form': form}

    return render(request, 'base/create-room.html', context)

@login_required(login_url='login')
def update_room(request, pk):

    room = Room.objects.get(id=pk)
    form = Roomform(instance=room)


    if request.user == room.host or request.user.username == 'admin':
        if request.method == 'POST':
            form = Roomform(request.POST ,instance=room)

            if form.is_valid:
                form.save()

                return redirect('home')

        context = {'form': form}

        return render(request, 'base/update-room.html', context)
    else:
        return HttpResponse('You are not allowed to do that!')



@login_required(login_url='login')
def delete_room(request,pk):
    room = Room.objects.get(id=pk)

    if request.user == room.host or request.user.username == 'admin':
        
        if request.method == 'POST':
            room.delete()
            return redirect('home')

        context = {'room': room}

        return render(request, 'base/delete-room.html', context)
    else:
        return HttpResponse('You are not allowed to do that!')



def login_user(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try :
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist, sign up first')
            return redirect('register')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'You are logged in now')
            return redirect('home')
        else:
            messages.error(request,'Please check again your credentials')
            return redirect('login')

    context={'page' : page}

    return render(request,'base/login_register.html', context)


def logout_user(request):

    logout(request)
    return redirect('login')
    

def register_user(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
           user = form.save(commit=False)
           user.save()
           login(request,user)

           return redirect('home')
        else:
            messages.error(request,'An error occured during registration')
            return redirect('register')

    context = {'form': form}

    return render(request,'base/login_register.html', context)


@login_required(login_url='login')
def delete_room_message(request,pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed to do that!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    context = {'room': message}

    return render(request, 'base/delete-room.html', context)