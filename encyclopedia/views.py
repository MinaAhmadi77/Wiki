
from django.shortcuts import render
import markdown2
from . import util
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.db import models
from django.db.models import Model
import random
import logging


class NewTaskForm(forms.Form):
    task = forms.CharField(label="request")
    # priority = forms.IntegerField(label="Priority", min_value=1, max_value=5)
class NewEncyclopedia(forms.Form):
    title=forms.CharField(widget=forms.TextInput(attrs={'name':'title'}))
    content= forms.CharField(widget=forms.Textarea(attrs={'name':'text', 'style': 'height: 25em;'}))
class Update(forms.Form):
    content= forms.CharField(widget=forms.Textarea(attrs={'name':'text', 'style': 'height: 25em;'})) 
def index(request):
    flag=False
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            name_page = form.cleaned_data["task"] 
            listOfEntries=util.list_entries()
            if name_page in listOfEntries:   
                return redirect('showPage', page=name_page )
            else :
               
                new_listOfEntries = [s for s in listOfEntries if name_page in s]
                return render(request, "encyclopedia/index.html", {
                    "flag":True,
                    "form": form ,
                    "entries": new_listOfEntries
                })
        else:
            return render(request, "encyclopedia/index.html", {

                "flag":flag,
                "form": form
            })   
    
    return render(request, "encyclopedia/index.html", {
        "flag":flag ,
        "form": NewTaskForm() ,
        "entries": util.list_entries()
    })

def showPage(request,page):
    listOfEntries=util.list_entries()
    if page in listOfEntries:   
        return render(request, "encyclopedia/showPage.html", {
        "title":page,
        "form": NewTaskForm() ,
        "text": markdown2.markdown(util.get_entry(page)) 
    })
    else :
        return render(request, "encyclopedia/notfound.html", {

            "form": NewTaskForm() 

        })
    


def create(request):
    flag=False
    if request.method == "POST":
        form = NewEncyclopedia(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            listOfEntries=util.list_entries()
            if title in listOfEntries:   
                return render(request, "encyclopedia/create.html", {
                    "flag":True,
                    "form": NewTaskForm() ,
                    "add_new": form                
                })               
            else :
                util.save_entry(title,content)
                return redirect('showPage', page=title )

        else:
            return render(request, "encyclopedia/create.html", {

                "flag":flag,
                "form": NewTaskForm() ,
                "add_new": form
            })   
    
    return render(request, "encyclopedia/create.html", {
        
        "form": NewTaskForm() ,
        "add_new": NewEncyclopedia() 
        
    })   

def randomPage(request):
    list=util.list_entries()
    rand_entries = random.choice(list)
    return redirect('showPage',rand_entries)

def update(request,page):
    title=page
    flag=False
    if request.method == "POST":
       
        form=Update(request.POST)
        if form.is_valid():           
            content = form.cleaned_data["content"]
            util.save_entry(title,content)
            return redirect('showPage', page=title )

        else:
            return render(request, "encyclopedia/update.html", {

                "flag":True,
                "form": NewTaskForm(),
                "update":form
                
                
            })   
    u=Update()
    u.initial["content"]=util.get_entry(title)
    
    return render(request, "encyclopedia/update.html", {

        "title":title,
        "form": NewTaskForm() ,
        "update":u
        
    })   
       