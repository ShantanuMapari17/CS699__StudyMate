from email import message
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Room,Topic,Message,Profile
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RoomForm,MyUserForm,ProfileUpdateForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test


# Create your views here.

# login functionality------------------------------------------------------------------
def loginPage(request):
    page= 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method =='POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User Does not exits')

        user =authenticate(request,username=username, password=password)
        
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Username and Password does not match or user doesn\'t exist')
        

    context={'page':page}
    return render(request,'base/login_register.html',context)
# -------------------------------------------------------------------------------


# logout functionality--------------------------------------------------------
def logoutUser(request):
    logout(request)
    return redirect('home')
# ----------------------------------------------------------------------------


# user registration---------------------------------------------------------------
def registerUser(request):
    if request.method=='POST':
        f_name=request.POST.get('f_name')
        l_name=request.POST.get('l_name')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        u_name=request.POST.get('u_name')

        if User.objects.filter(username=u_name).exists():
            messages.error(request,"Username already taken . Try different")
            return redirect('register')

        elif User.objects.filter(email=email).exists():
            messages.error(request,"Email already present. Try different")
            return redirect('register')

        elif pass1!=pass2:
            messages.error(request,"Password not matching")
            return redirect('register')

        else:            
            user=User.objects.create(username=u_name, first_name=f_name, last_name=l_name, email=email, password=pass1)
            user.save()
            user.set_password(pass1)
            user.save()
            profile = Profile(user=user)
            profile.save()
            messages.success(request,"Registered Successfully")
            print("\n registration successful!!\n")
            return redirect('login')

    return render(request,'base/login_register.html')

# ---------------------------------------------------------------------------------



# main home page function-----------------------------------------------------------
def home(request):
    # filter the post on the basis of the query by user
    if request.GET.get('q') != None:
        q=request.GET.get('q')
    else:
        q=''

    # can be filtered on the basis of various parameters
    rooms = Room.objects.filter(
        Q(topic__name__icontains =q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )

    # for activity feed
    room_comments = Message.objects.filter(Q(room__topic__name__icontains=q)).order_by('-created')[0:5]
    
    # For topics in the feed
    topics = Topic.objects.all()

    room_count = rooms.count()  #room count 
    
    context={}
    context['rooms']=rooms
    context['topics']=topics
    context['room_count']=room_count
    context['room_comments']=room_comments
    
    return render(request, 'base/home.html' , context)
# -----------------------------------------------------------------------------------



# ----Room Page---------------------------------------------------
def room(request,pk):
    room=None
    room=Room.objects.get(id=pk)
    comments=room.message_set.all().order_by('-created')
    # print(room.description)
    room_participants = room.participants.all()
    room_likes=room.likes.all()
    room_likes_count=room_likes.count()

    flag=False
    if room.likes.filter(id=request.user.id).exists():
        flag=True

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST['msg_body'],
        )


        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    dict={}
    dict['room']=room
    dict['comments']=comments
    dict['room_participants']=room_participants
    dict['room_likes']=room_likes
    dict['room_likes_count']=room_likes_count
    dict['flag']=flag

    return render(request,'base/room.html', dict)
# ---------------------------------------------------------------------------------


# Create room Function-------------------------------------------------------------
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()

    if request.method =='POST':
        form = RoomForm(request.POST)
        if form.is_valid():

            room=form.save(commit=False)
            room.host = request.user

            room.save()
            return redirect('home')

    dict={}
    dict['form']=form
    return render(request,'base/room_form.html',dict)
# ---------------------------------------------------------------------------------


# Update room function------------------------------------------------------------
@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form=RoomForm(instance=room)

    if request.user != room.host :
        return HttpResponse("You are not allowed here!!")

    if request.method =='POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    dict={}
    dict['form']=form
    return render(request, 'base/room_form.html',dict)
# -------------------------------------------------------------------------------------


# delete the room----------------------------------------------------------------------
@login_required(login_url='login')
def deleteRoom(request,pk):
    room= Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You can not delete this room!!")
    
    if request.method=='POST':
        room.delete()

        return redirect('home')

    dict={}
    dict['obj']=room
    return render(request,'base/delete.html',dict)
# ------------------------------------------------------------------------------------


# delete message functionality--------------------------------------------------------
# login is required for a message to be deleted
@login_required(login_url='login')
def deleteComment(request, p_key):
    comment=Message.objects.get(id=p_key)

    # if user is not the one who did the message
    if request.user != comment.user:
        return HttpResponse('You are not permitted to delete the message')

    if request.method == 'POST':
        comment.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj':comment})
# --------------------------------------------------------------------------------------



# USER PROFILE ---------------------------------------------------------------------
def userProfile(request,p_key):
    user=User.objects.get(id=p_key)
    followers=user.profile.follower.all()
    followers_count=user.profile.follower.count()
    # get all the entries of the child user---->room
    rooms = user.room_set.all()

    room_comments= user.message_set.all()

    topics= Topic.objects.all()

    flag=False
    if user.profile.follower.filter(id=request.user.id).exists():
        flag=True

    dict={}
    dict['user']=user
    dict['rooms']=rooms
    dict['room_comments']=room_comments
    dict['topics']=topics
    dict['followers']=followers
    dict['followers_count']=followers_count
    dict['flag']=flag
    return render(request, 'base/user_profile.html',dict)
#---------------------------------------------------------------------------------------


# UPDATE USER---------------------------------------------------------------------------
@login_required(login_url='login')
def updateUser(request):
    form = MyUserForm(instance=request.user)
    profile_form= ProfileUpdateForm(instance=request.user.profile)
    # import pdb;pdb.set_trace()

    if request.method == 'POST' :
        form= MyUserForm(request.POST,instance=request.user)
        profile_form= ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)

        if form.is_valid() and profile_form.is_valid() :
            form.save()
            profile_form.save()
            return redirect('user_profile', p_key=request.user.id)

    dict={}
    dict['form']=form
    dict['profile_form']=profile_form
    return render(request,'base/user-update.html',dict)
# ===================================================================================


#Room-Likes Feature=================================================================
def RoomLike(request,pk):
    room=Room.objects.get(id=pk)

    if room.likes.filter(id=request.user.id).exists():
        room.likes.remove(request.user)
    else:
        room.likes.add(request.user)
    
    return redirect('room',pk=room.id)
# ================================================================================


# view all users===================================================================

def AllUsers(request):

    if request.GET.get('q') != None:
        q=request.GET.get('q')
    else:
        q=''

    users = User.objects.filter(
        Q(username__icontains =q) |
        Q(first_name__icontains=q) |
        Q(last_name__icontains=q)
        )
    
    # users=User.objects.all()

    dict={}
    dict['users']=users

    return render(request,'base/all_users.html',dict)

# =================================================================================
    

# Create Topics==================================================================
def CreateTopics(request):
    if request.method=='POST':
        topic_name=request.POST['topic_name']

        if Topic.objects.filter(name=topic_name).exists():
            messages.error(request,"Topic Already Exists")
            return redirect('home')
        else:
            topic=Topic.objects.create(name=topic_name)
            topic.author=request.user
            topic.save()
            messages.success(request,"Topic Created Successfully")
            return redirect('home')
    
    dict={}
    return render(request,'base/topic_form.html',dict)

# ==============================================================================

#Add follower===================================================================
def AddFollower(request,pk):
    user=User.objects.get(id=pk)

    if user.profile.follower.filter(id=request.user.id).exists():
        user.profile.follower.remove(request.user)
    else:
        user.profile.follower.add(request.user)
    
    return redirect('user_profile',pk)

# =============================================================================