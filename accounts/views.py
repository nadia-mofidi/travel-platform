from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from accounts.forms import SignupForm,UserProfileForm,ProfileForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from utils.messages import error_message,success_message
from django.utils.http import url_has_allowed_host_and_scheme
# Create your views here.
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method=='POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            success_message(request, 'Your account has been created successfully! Welcome to our travel community.')
            return redirect('accounts:login')
        else:
            error_message(request, 'We couldn’t create your account. Please check the form and try again.')
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
            user = form.get_user()
            login(request, user)

            success_message(request, 'Welcome back! You have successfully logged in.')
            next_url = request.POST.get('next')

            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()}
            ):
                return redirect(next_url)
            
            return redirect('/')
        else:
            error_message(request, 'Couldn\'t log you in. Please try again.')
    else:
        form = AuthenticationForm()

    context = {'form':form,'next':request.GET.get('next')}
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

            profile = request.user.profile

            uploaded_avatar = request.FILES.get('avatar')
            selected_preset = request.POST.get('avatar_preset')

            old_avatar = profile.avatar.name if profile.avatar else None

            user_form.save()
            profile_form.save()

            # Preset has priority
            if selected_preset:

                if old_avatar and profile.avatar:
                    profile.avatar.delete(save=False)

                profile.avatar = None
                profile.avatar_preset = selected_preset
                profile.save()

            # Custom uploaded avatar
            elif uploaded_avatar:

                profile.avatar_preset = ''
                profile.save()

            success_message(
                request,
                'Your profile has been updated successfully!'
            )

            return redirect('accounts:profile')

        else:
            error_message(
                request,
                'We couldn’t update your profile. Please check the form and try again.'
            )

    else:

        user_form = UserProfileForm(
            instance=request.user
        )

        profile_form = ProfileForm(
            instance=request.user.profile,
            is_author=is_author
        )

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'is_author': is_author
    }

    return render(
        request,
        'accounts/edit-profile.html',
        context
    )

@login_required
def profile_view(request):
    is_author = request.user.groups.filter(name='Authors').exists()

    context = {'is_author': is_author,}

    return render(request,'accounts/profile.html',context)