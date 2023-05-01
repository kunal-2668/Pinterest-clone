"""Pinterest_Clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Pins import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Pinterest_home,name='home'),
    path('add_pin',views.add_pin,name='add_pin'),
    path('signup',views.Signup,name='signup'),
    path('login',views.Login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('addprofile',views.addprofile,name='addprofile'),
    path('profile',views.Profile_page,name='profile'),
    path('update_profile<int:id>',views.update_profile,name='update_profile'),
    path('search',views.searchPin,name='search'),
    path('readMore/<int:id>',views.readMore,name='readMore'),
    path('CommentBox',views.CommentBox,name='Commentbox'),
    path('DeleteCommentById/<int:id>/<int:postid>',views.DeleteCommentById,name='deletecomment'),
    path('LikePin/<int:id>',views.LikePin,name='LikePin'),

]
