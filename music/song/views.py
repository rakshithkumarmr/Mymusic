from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Song, Listenlater,History,Channel
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.db.models import Case,When
from django.contrib.auth import logout
from django.db.models import Q
import re


def HomePage(request):
    song = Song.objects.all()
    ids = []
    for x in song:
        ids.append(x.song_id)
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    song = Song.objects.filter(song_id__in=ids).order_by(preserved).reverse()
    song = song[0:3]
    if request.user.is_authenticated:
        ll = Listenlater.objects.filter(user=request.user)
        ids = []
        for x in ll:
            ids.append(x.audio_id)
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
        watch = Song.objects.filter(song_id__in=ids).order_by(preserved).reverse()
        watch = watch[0:3]
        return render(request, "song/home.html", {'song': song, 'watch': watch})
    return render(request,"song/home.html",{'song':song})


def All_songs(request):
    song = Song.objects.all()
    ids = []
    for x in song:
        ids.append(x.song_id)
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    song = Song.objects.filter(song_id__in=ids).order_by(preserved).reverse()
    paginator = Paginator(song,per_page=6)
    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)
    return render(request, "song/all_song.html", {'song': page_obj.object_list,'paginator':paginator})


def songpost(request,id):
    song = Song.objects.filter(song_id=id).first()
    return render(request, "song/songpost.html", {'song': song})


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            from django.contrib.auth import login
            login(request,user)
            return redirect('/')
        else:
            message = "Invalid username or password"
            return render(request, "song/login.html",{"mess":message})
    return render(request, "song/login.html")

def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if User.objects.filter(username=username).exists():
            messages.error(request,"Username is  already taken. pleasetry another one !")
            return redirect('signup')
        if len(username) > 15:
            messages.error(request,"Username must be less tahn 15 characters")
            return redirect('signup')
        if not username.isalnum():
            messages.error(request,"Username should only contain letters and numbers")
            return redirect('signup')
        if pass1 != pass2:
            messages.error(request,"Password Do not Match")
            return redirect('signup')
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        pat = re.compile(reg)
        mat = re.search(pat, pass1)
        if len(pass1) >5 and len(pass1) < 21:
            if mat:
                myuser = User.objects.create_user(username=username,email=email,password=pass1)
                myuser.first_name = firstname
                myuser.last_name = lastname
                myuser.save()
                channel = Channel(name=username)
                channel.save()
                messages.error(request, "Successfully registerd Your Account")
                return redirect('login')
            else:
                messages.error(request,"Password should have at least one uppercase letter,lowercse,one number and one special symbol.")
                return redirect('signup')
        else:
            messages.error(request, "Password lengnth shoul be 6-20.")
            return redirect('signup')
    return render(request, "song/signup.html")


def listen_later(request):
    if request.user.is_authenticated == True:
        if request.method == "POST":
            user = request.user
            audio = request.POST['song']
            listen = Listenlater.objects.filter(user=user)
            for x in listen:
                if audio == x.audio_id:
                    message = "Your audio is already added"
                    break
            else:
                listenlater = Listenlater(user=user,audio_id=audio)
                listenlater.save()
                message = "Your audio is successfully added"
            song = Song.objects.filter(song_id=audio).first()
            return render(request,f"song/songpost.html",{'song':song,"message":message})
        ll = Listenlater.objects.filter(user=request.user)
        ids = []
        for x in ll:
            ids.append(x.audio_id)
        preserved = Case(*[When(pk=pk,then=pos) for pos,pk in enumerate(ids)])
        song = Song.objects.filter(song_id__in=ids).order_by(preserved).reverse()
        paginator = Paginator(song, per_page=6)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request,"song/listen_later.html",{'song': page_obj.object_list,'paginator':paginator})
    else:
        return redirect('login')

def logout_user(request):
    logout(request)
    return redirect('/')


def history(request):
    if request.user.is_authenticated == True:
        if request.method == "POST":
            user = request.user
            audio_id = request.POST['audio_id']
            history = History(user=user, audio_id=audio_id)
            history.save()
            return redirect(f'/songpost/{audio_id}')
        history = History.objects.filter(user=request.user)
        ids = []
        for x in history:
            ids.append(x.audio_id)
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
        song = Song.objects.filter(song_id__in=ids).order_by(preserved).reverse()
        paginator = Paginator(song, per_page=6)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request,'song/history.html',{'song': page_obj.object_list,'paginator':paginator})
    else:
        return redirect('login')


def channel(request):
    if request.user.is_authenticated == True:
        chan = Channel.objects.filter(name=request.user)
        song1 = []
        for x in chan:
            if x.music:
                song = Song.objects.filter(song_id=int(x.music))
                song1.append(song)
        return render(request,'song/channel.html',{'channel':request.user,'song': song1,'paginator':''})
    else:
        return redirect('login')

def upload_music(request):
    if request.user.is_authenticated == True:
        if request.method == "POST":
            name = request.POST['name']
            singer = request.POST['singer']
            tag = request.POST['tag']
            image = request.FILES['image']
            moviename = request.POST['moviename']
            song = request.FILES['song']
            song_model = Song(name=name,singer=singer,tags=tag,image=image,movie_name=moviename,song=song)
            try:
                song_model.save()
                music_id = song_model.song_id
                channel_model= Channel(name=request.user,music=music_id)
                channel_model.save()
                messages.success(request, "successfully uploaded")
                return render(request, 'song/upload_music.html')
            except:
                mess = "Something went wrong"
                return render(request, 'song/upload_music.html',{"mess":mess})
        return render(request, 'song/upload_music.html')
    else:
        return redirect('login')

def search(request):
    search = request.POST['search']
    if search:
        match = Song.objects.filter(Q(name__icontains=search))
        if match:
            return render(request, "song/search.html", {"song": match})
        else:
            messages.success(request, "search not found")
            return render(request, "song/search.html")


def ll_delete(request,id):
    if request.user.is_authenticated == True:
        song = Listenlater.objects.filter(audio_id=id).delete()
        messages.success(request, "successfully removed")
        return redirect('listen_later')
    else:
        return redirect('login')

def history_delete(request,id):
    if request.user.is_authenticated == True:
        song = History.objects.filter(audio_id=id).delete()
        messages.success(request, "successfully removed")
        return redirect('history')
    else:
        return redirect('login')

def channel_song_delete(request,id):
    if request.user.is_authenticated == True:
        song = Song.objects.filter(song_id=id).delete()
        messages.success(request, "successfully removed")
        return redirect('channel')
    else:
        return redirect('login')