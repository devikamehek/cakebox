from django.shortcuts import render,redirect
from django import forms
from myapp.models import Cake
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages


# Create your views here.
# create,retrive(list,detail),update,delete 

class CakeForm(forms.ModelForm):
    class Meta:
        model=Cake
        fields=["name","flavour","price","shape","weight","layer","cake_pic","description"]

        widgets={
            # "user":forms.TextInput(attrs={"class":"form-control"}),
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "flavour":forms.TextInput(attrs={"class":"form-control"}),
            "price":forms.NumberInput(attrs={"class":"form-control"}),
            "shape":forms.TextInput(attrs={"class":"form-control"}),
            "weight":forms.NumberInput(attrs={"class":"form-control"}),
            "layer":forms.NumberInput(attrs={"class":"form-control"}),
            "cake_pic":forms.FileInput(attrs={"class":"form-control"}),
            "description":forms.Textarea(attrs={"class":"form-control","rows":2})
        }



class RegistrationForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    class Meta:
        model=User
        fields=["first_name","last_name","email","username","password1","password2"]

        widgets={
            "first_name":forms.TextInput(attrs={"class":"form-control"}),
            "last_name":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "password1":forms.PasswordInput(attrs={"class":"form-control"})
        }




class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))





class CakeCreateView(View):
    def get(self,request,*args,**kwargs):
        form=CakeForm()
        return render(request,"cake-add.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=CakeForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            Cake.objects.create(**form.cleaned_data,user=request.user)
            messages.success(request,"Cake added succesfully")
            return redirect("cake-list")
        messages.error(request,"Cake failed to add")
        return render(request,"cake-add.html",{"form":form})
    

class CakeListView(View):
    def get(self,request,*args,**kwargs):
        qs=Cake.objects.filter(user=request.user)
        return render(request,"cake-list.html",{"cakes":qs})
    

class CakeDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Cake.objects.get(id=id)
        return render(request,"cake-detail.html",{"cake":qs})
    

class CakeDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Cake.objects.get(id=id).delete()
        messages.success(request,"Cake removed succesfully")
        return redirect("cake-list")
    

class CakeEditView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        c=Cake.objects.get(id=id)
        form=CakeForm(instance=c)
        return render(request,"cake-edit.html",{"form":form})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        c=Cake.objects.get(id=id)
        form=CakeForm(instance=c,data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Cake edited succesfully")
            return redirect("cake-detail",pk=id)
        messages.error(request,)
        return render(request,"cake-edit.html",{"form":form})
    


class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Account created succesfully")
            return redirect("signin")
        messages.error(request,"request failed")
        return render(request,"register.html",{"form":form})
    





class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"Login succesfull")
                return redirect("cake-list")
            messages.error(request,"invalid credentials")
        return render(request,"login.html",{"form":form})
    


def signout_view(request,*args,**kwargs):
    logout(request)
    return redirect("signin")

    



