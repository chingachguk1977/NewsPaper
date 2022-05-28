from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group, User
from django.forms import ModelForm


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user


class UpdateProfileForm(ModelForm):
    class Meta:
        model = User
        # тут добавляем поля на форму апдейта профиля (profile_update.html)
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'groups',
        ]
# TODO добавить поля с подписками и группами, попытаться реализовать возможность их тут же редактировать
# попытаться избавиться от лейблов полей
