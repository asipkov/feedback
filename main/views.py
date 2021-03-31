from django.shortcuts import render
from .forms import LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth import models
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import ProfileEditFormUser, ProfileEditFormUserProfile
from .models import UserProfile
from django.contrib.auth.models import Group
from .forms import CommentForm
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User


def main(request):
    return render(request, 'main/main.html')


def register(request):
    return render(request, 'main/register.html')


def my_profile(request, user_id):
    user = get_object_or_404(models.User, id=user_id)
    comments = user.comments.all()
    return render(request,
                  'main/my_profile.html',
                  {'user': user,
                   'comments': comments,
                   })

def profile(request, user_id):
    user = get_object_or_404(models.User, id=user_id)
    comments = user.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = user
            new_comment.name = request.user.username
            new_comment.save()
            return HttpResponseRedirect(f'/id{user_id}')
    else:
        comment_form = CommentForm()
    return render(request,
                  'main/profile.html',
                  {'user': user,
                   'comments': comments,
                   'comment_form': comment_form, })


class Ratings(DetailView):

    def get_context_data(self):
        rait = UserProfile.objects.filter(ratings__isnull=False).order_by('ratings__average').reverse
        return rait()

    def get(self, request):
        result_raiting = []
        for el in Ratings.get_context_data(self):
            user_rait = User.objects.get(id=el.user_id)
            group = Group.objects.get(name='worker')
            if group in user_rait.groups.all():
                result_raiting.append(user_rait)
        return render(request, 'main/ratings.html', {'result_raiting': result_raiting})


class LoginView(View):

    def get(self, request):
        form = LoginForm(request.POST or None)
        return render(request, 'main/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'main/login.html', {'form': form})


class RegistrationView(View):

    def get(self, request):
        form = RegistrationForm(request.POST or None)
        return render(request, 'main/registration.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST, request.FILES or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            group = Group.objects.get(name="guest")
            new_user.groups.add(group)
            new_profile = UserProfile()
            new_profile.user = new_user
            new_profile.phone_number = form.cleaned_data['phone_number']
            new_profile.avatar = form.cleaned_data['avatar']
            new_profile.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        return render(request, 'main/registration.html', {'form': form})


@login_required
def edit(request, id):
    user = get_object_or_404(models.User, id=id)
    userprofile = get_object_or_404(UserProfile, id=id)
    if request.method != 'POST':
        form = ProfileEditFormUser(instance=user, prefix='form')
        form2 = ProfileEditFormUserProfile(instance=userprofile, prefix='form2')
        request.session['return_path'] = request.META.get('HTTP_REFERER', '/')
    else:
        form = ProfileEditFormUser(request.POST, instance=user, prefix='form')
        form2 = ProfileEditFormUserProfile(request.POST, request.FILES, instance=userprofile, prefix='form2')
        if form.is_valid() and form2.is_valid():
            user = form.save(commit=False)
            user.save()
            userprofile = form2.save(commit=False)
            userprofile.save()
        return HttpResponseRedirect(request.session['return_path'])
    context = {'form': form, 'form2': form2}
    return render(request, 'main/edit.html', context)



