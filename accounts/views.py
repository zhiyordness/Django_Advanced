from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import user_passes_test, permission_required, login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import logout_then_login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from accounts.forms import CustomUserCreationForm, SetUnusablePasswordForm

UserModel = get_user_model()

@user_passes_test(lambda u: not u.is_authenticated, login_url=reverse_lazy('home'))
def register_fbv(request: HttpRequest):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("home")

    return render(request, 'accounts/register.html', {"form": form})


class RegisterView(UserPassesTestMixin, CreateView):
    form_class = CustomUserCreationForm
    model = UserModel
    template_name = 'accounts/register.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def test_func(self):
        return not self.request.user.is_authenticated


def login_fbv(request: HttpRequest) -> HttpResponse:
    # username = request.POST.get('username')
    # password = request.POST.get('password')
    # user = authenticate(request, username=username, password=password)

    # if user:
    #     login(request, user)
    #     return redirect('home')

    form = AuthenticationForm(request, request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect('home')

    return render(request, 'accounts/login.html', {"form": form})


def logout_fbv(request: HttpRequest):
    if request.method == "POST":
        logout(request)
    return logout_then_login(request)


class ProfileDetailView(TemplateView):
    template_name = 'accounts/profile_details.html'


@login_required
@permission_required('auth.can_set_unusable_password')
def set_unusable_password(request: HttpRequest) -> HttpResponse:
    form = SetUnusablePasswordForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        selected_user = form.cleaned_data['user']
        if selected_user.is_superuser:
            messages.error(request, "You cannot set an unusable password for a superuser.")
            return redirect('home')
        selected_user.set_unusable_password()
        selected_user.save(update_fields=['password'])
        messages.success(request, f"Password for user {selected_user.get_username()} has been set to unusable.")
        return redirect('home')

    return render(request, 'accounts/set_unusable_password.html', {"form": form})
