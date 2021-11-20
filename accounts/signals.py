from allauth.account.signals import user_signed_up
from django.dispatch.dispatcher import receiver
from django.shortcuts import redirect, render

@receiver(user_signed_up)
def profile(request, user, **kwargs):
    print(dir(user))

    return redirect('community:index')