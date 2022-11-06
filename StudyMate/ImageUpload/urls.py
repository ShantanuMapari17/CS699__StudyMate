from django.urls import path,include
from . import views

urlpatterns=[ 
    path('imagehome/',views.imagehome,name='imagehome'),
    path('upload-img/',views.uploadImage,name='upload-img'),
]