from dataclasses import field
import imp
from pyexpat import model
from django.forms import ModelForm,TextInput,EmailInput,ImageField,FileInput,Textarea
from .models import Room,Profile,Topic
from django import forms
from django.contrib.auth.models import User

class RoomForm(ModelForm):
    # name=forms.CharField(max_length=200,required=True)
    description=forms.Textarea()
    class Meta:
        model=Room
        fields = [  'topic',
                    'name',
                    'description',
                ]


class MyUserForm(ModelForm):
    class Meta:
        model=User
        fields=['first_name',
                'last_name',
                'username',
                'email',
                ]
        
        widgets ={
            'first_name': TextInput(attrs={
                'class':"form-control",
                'placeholder':"First Name",
                'style': 'max-width: 300px;',
            }),
            'last_name': TextInput(attrs={
                'class':"form-control",
                'placeholder':"Last Name",
                'style': 'max-width: 300px;',
            }),
            'email': EmailInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Email'
                }),
            'username': TextInput(attrs={
                'class':"form-control",
                'placeholder':"UserName",
                'style': 'max-width: 300px;',
                'disabled':'True',
            }),
        }



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio',
                    'profile_pic',]

        widgets ={
            'profile_pic':FileInput(attrs={
                'class':"form-control",
                'style': 'max-width: 300px;',
            }),
            'bio':Textarea(attrs={
                'class':"form-control",
                'placeholder':"Bio",
                'style': 'max-width: 300px;',
            }),
        }





        