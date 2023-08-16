from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('signup',views.signup, name='signup'),
    path('login',views.loginUser, name='login'),
    path('logout',views.logoutUser, name='logout'),
    path('settings',views.settings, name='settings'),
    path('upload',views.upload,name='upload'),
    path('like-post',views.like_post,name='like-post'),
    path('profile/<str:pk>',views.profile,name='profile'),   #pk is a name and its datatype is a str
    path('follow',views.follow,name='follow'),
    path('search',views.search,name='search'),
    path('delete',views.delete,name='delete')
]