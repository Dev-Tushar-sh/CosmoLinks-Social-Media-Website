from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .models import Profile,Post, LikePost, FollowersCount

from django.contrib.auth.decorators import login_required

from itertools import chain
import random

# Create your views here.

@login_required(login_url='/login')
def index(request):
    user_object = User.objects.get(username = request.user)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower = request.user.username)

    for users in user_following:
        user_following_list.append(users.user)
    
    for username in user_following_list:
        feed_lists = Post.objects.filter(user=username)
        feed.append(feed_lists)
    
    feed_list = list(chain(*feed))   #query set ko list me convert krr diya

    # users suggestions

    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]

    currend_user = User.objects.filter(username=request.user.username)
    final_suggestions_list =[ x for x in list(new_suggestions_list) if (x not in list(currend_user))]

    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list= []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_list = Profile.objects.filter(user_id=ids)
        username_profile_list.append(profile_list)
    
    suggestions_username_profile_list = list(chain(*username_profile_list))

    suggestions_username_profile_list = list(chain(*username_profile_list))
    return render(request,'index.html',{'user_profile':user_profile, 'posts':feed_list,'suggestions_username_profile_list':suggestions_username_profile_list[:4]})

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                #log user in and redirect to settings page
                
                user_login = authenticate(username=username,password=password1)
                login(request,user_login)

                #create a profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model)
                new_profile.save()
                messages.success(request,"Account created Successfully")
                return redirect('settings')

        else:
            messages.info(request,'Password Not Matching')
            return redirect('signup')
                
    else:
        return render(request,'signup.html')

def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Credentials Ivalid')
            return redirect('login')

    else:
        return render(request,'login.html')
    
def logoutUser(request):
    logout(request)
    return redirect('login')

def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        print("request i hai")

        if request.FILES.get('imagedp') == None:   #user try to update the image and other info
            image = user_profile.profile_img        # if its none no image is been sent
            bio = request.POST['bio']
            location = request.POST['location']
            
            user_profile.profile_img =image         
            user_profile.bio = bio         
            user_profile.location = location   
            user_profile.save()

        if request.FILES.get('imagedp') != None:
            # print(bio,location)
            image = request.FILES.get('imagedp')
            bio = request.POST['bio']
            location = request.POST['location']
            
            user_profile.profile_img =image         
            user_profile.bio = bio         
            user_profile.location = location         
            user_profile.save()

        return redirect('settings')
    return render(request,'setting.html',{'user_profile':user_profile})

@login_required(login_url='/login')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        new_post = Post.objects.create(user=user,image=image, caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='/login')
def like_post(request):

    username = request.user.username
    post_id = request.GET.get('post_id')   #hamne ye direct isiliye likha hai kyoki index.html se
#                                           ye direct post method se sen kii hue hai line 263 k ass pass
    post = Post.objects.get(id=post_id)
    
    like_filter = LikePost.objects.filter(post_id=post_id, username = username ).first() #filter se sare aajayenge 
    #jabki get function se sirf ek object aayega

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1   #post me whi object pda hai tho isliye post.like +1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        return redirect('/')

@login_required(login_url='/login')
def profile(request,pk):

    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user = user_object)
    user_posts = Post.objects.filter(user=pk)       #dhyan rakho yaha post dekh rahe hai profile nahi
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower,user=user).first():
        button_text = 'Unfollow'
    else:
        button_text= 'Follow'

    user_follower = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {'user_object':user_object,
               'user_profile':user_profile,
               'user_posts':user_posts,
               'user_post_length':user_post_length,
               'button_text':button_text,
               'user_follower':user_follower,
               'user_following':user_following

    }

    return render(request,'profile.html',context)

@login_required(login_url='/login')
def follow(request):

    if request.method == 'POST':
        follower = request.POST['follower']                     #person that is following someone else
        user = request.POST['user']                     #person that is following someone else

        if FollowersCount.objects.filter(follower=follower , user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user= user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower = follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
         
    else:
        return redirect('/')
    
@login_required(login_url='/login')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        searchitem = request.POST['username']
        username_object = User.objects.filter(username__icontains = username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(user_id = ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))
    return render(request,'search.html',{'user_profile':user_profile,'username_profile_list':username_profile_list,'searchitem':searchitem})

def delete(request):
    postuser = request.GET.get('deletepost')
    print("adsfadsfasdfadsfasdfasdfsadfdsaf54sad6f4sad5f46d5sa4fdsa4f54dsaf654sadf")
    print(request.user.username)
    print(postuser)
    post = Post.objects.get(id = postuser)
    post.delete()
    return redirect('/')

