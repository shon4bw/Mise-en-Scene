from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods

from accounts.models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.http import JsonResponse
from community.models import Review
from django.core.paginator import Paginator

import os

@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('community:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('community:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('movies:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'movies:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@require_POST
def logout(request):
    auth_logout(request)
    return render(request, 'accounts/logout.html')


@login_required
def profile(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    is_following = person.followings.filter(pk=request.user.pk).exists()
    articles = Review.objects.filter(user_id=person.id).order_by('-pk')

    page = int(request.GET.get('p', 1)) #????????? 1??? ??????
    paginator = Paginator(articles, 5) #??? ????????? ??? ?????? ??? ????????? ??? ?????? 
    boards = paginator.get_page(page)

    context = {
        'person': person,
        'is_following': is_following,
        'articles': boards,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def update(request, user_pk):
    '''
    GET: "???????????? ?????? ???" ??????
    POST: ????????? ???????????? ????????? ?????? ??? ??????
    '''

    user = User.objects.get(pk=user_pk)
    
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', user.username)
    else:
        form = CustomUserChangeForm(instance=user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)


@require_POST
def follow(request, user_pk):
    if request.user.is_authenticated:

        person = get_object_or_404(get_user_model(), pk=user_pk)
        user = request.user
        if person != user:
            if person.followers.filter(pk=user.pk).exists():
                # ????????????
                person.followers.remove(user)
                followed = False
            else:
                # ?????????
                person.followers.add(user)
                followed = True

            context = {
                'followed' : followed,
                'following_count' : person.followings.count(),
                'follower_count' : person.followers.count(),
            }
            return JsonResponse(context)

def kakao_login(request):
    app_key= os.environ.get("42a0571fe9d27ca9810a5e953a9f87fc")
    redirect_uri = 'http://localhost:8000/accounts/kakao/login/callback/'
    kakao_auth_api = 'https://kauth.kakao.com/oauth/authorize?response_type=code'
    return redirect (f'{kakao_auth_api}&client_id={app_key}&redirect_uri={redirect_uri}')


