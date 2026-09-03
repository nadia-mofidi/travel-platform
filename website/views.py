from django.shortcuts import render,redirect
from website.forms import ContactForm,NewsletterForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from utils.messages import success_message, error_message

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
            form.save()
            success_message(request,'Your ticket is submitted successfully')
            return redirect('/contact#form')
        else:
            error_message(request,'Your ticket couldn\'t be submitted')
            return render(request,'website/contact.html',{'form':form})
        
    form=ContactForm()
    return render(request,'website/contact.html',{'form':form})

def newsletter_view(request):
    if request.method=="POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            success_message(request, 'You have successfully subscribed to our newsletter!')
            return HttpResponseRedirect('/')
        else:
            error_message(request, 'We couldn’t subscribe you to the newsletter. Please try again.')
    else:
        return HttpResponseRedirect('/')
