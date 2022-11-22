from django.urls import path
from . import views

urlpatterns=[
    
    path('',views.home,name='home'),
    path('room/<str:pk>/',views.room,name='room'),
    path('profile/<str:p_key>' , views.userProfile, name='user_profile'),

    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),


    path('create-room/', views.createRoom , name='create-room'),
    path('update-room/<str:pk>/', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),

    path('delete-comment/<str:p_key>', views.deleteComment, name='delete-comment'),

    path('user-update/' , views.updateUser,  name="user-update"),

    path('room-like/<str:pk>' , views.RoomLike,name='room-like' ),

    path('all-users/',views.AllUsers,name='all-users'),

    path('add-follower/<str:pk>',views.AddFollower,name='add-follower'),

    path('create-topic/',views.CreateTopics,name='create-topic'),

    path('reset-password/',views.resetPassword,name='reset-password'),
    
]