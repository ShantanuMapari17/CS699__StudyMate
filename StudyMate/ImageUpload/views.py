from django.shortcuts import render

# Create your views here.
from email.mime import image
from django.shortcuts import render,redirect
from .forms import ImageForm

from .models import MyImage
# Create your views here.
def imagehome(request):
    imagesss=MyImage.objects.all()
        
    dict={'name':"Shantanu",'imagesss':imagesss}
    return render(request,'imagehome.html',dict)

def uploadImage(request):
    form=ImageForm()

    if request.method=='POST':
        form=ImageForm(request.POST,request.FILES)

        if form.is_valid():
            img=form.save()
            img.save()
            return redirect('home')
        
    dict={'form':form}

    return render(request,'upload.html',dict)