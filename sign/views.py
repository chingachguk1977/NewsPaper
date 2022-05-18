from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView, UpdateView

from .forms import UpdateProfileForm
from .models import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from news.models import Author


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(user=user)
    return redirect('/')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'profile_update.html'
    form_class = UpdateProfileForm
    success_url = '/posts/'
    success_message = 'User profile updated successfully.'

    # def setup(self, request, *args, **kwargs):
    #     self.user_id = request.user.pk
    #     return super().setup(request, *args, **kwargs)

    def get_object(self, **kwargs):
        return self.request.user

    # def get_success_url(self):
    #     return self.success_url


# @login_required
# def profile_update(request):
#     user = request.user
#     authors_group = Group.objects.get(name='authors')
#     if not request.user.groups.filter(name='authors').exists():
#         authors_group.user_set.add(user)
#     return redirect('/')
