from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from accounts.forms import SignupForm,UserProfileForm,ProfileForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method=='POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = SignupForm()
    context = {'form':form}
    return render(request,'accounts/signup.html',context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method=='POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username=username,password=password)
            if user is not None:
               login(request,user)
               return redirect('/')
    else:
        form = AuthenticationForm()
    context = {'form':form}
    return render(request,'accounts/login.html',context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def edit_profile_view(request):

    is_author = request.user.groups.filter(
        name='Authors'
    ).exists()

    if request.method == 'POST':

        user_form = UserProfileForm(
            request.POST,
            instance=request.user
        )

        profile_form = ProfileForm(
            request.POST,
            request.FILES,
            instance=request.user.profile,
            is_author=is_author
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return redirect('accounts:profile')

    else:

        user_form = UserProfileForm(instance=request.user)

        profile_form = ProfileForm(instance=request.user.profile,is_author=is_author)

    context = {'user_form': user_form,'profile_form': profile_form,'is_author': is_author}

    return render(request,'accounts/edit-profile.html',context)

@login_required
def profile_view(request):
    is_author = request.user.groups.filter(name='Authors').exists()

    context = {'is_author': is_author,}

    return render(request,'accounts/profile.html',context)