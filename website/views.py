from django.shortcuts import render,redirect
from website.forms import ContactForm,NewsletterForm
from django.http import HttpResponseRedirect
from django.contrib import messages

# Create your views here.
from django.http import HttpResponse
def index_view(request):
    return render(request,'website/index.html')

def about_view(request):
    return render(request,'website/about.html')

def contact_view(request):

    if request.method=="POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form_obj=form.save(commit=False)
            form_obj.name="Samira"
            form_obj.save()
            messages.add_message(request,messages.SUCCESS,'Your ticket is submitted successfully')
        else:
            messages.add_message(request,messages.ERROR,'Your ticket couldn\'t be submitted')
        return redirect('/contact#form')
    form=ContactForm()
    return render(request,'website/contact.html',{'form':form})

def newsletter_view(request):
    if request.method=="POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')
