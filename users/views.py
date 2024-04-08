from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from users.forms import UserCreateForm, ProfileUpdateForm


class RegisterView(View):
    @staticmethod
    def get(request):
        create_form = UserCreateForm()
        context = {
            "form": create_form
        }
        return render(request, 'users/register.html', context)

    @staticmethod
    def post(request):
        create_form = UserCreateForm(data=request.POST)

        if create_form.is_valid():
            create_form.save()
            return redirect('users:login')
        else:
            context = {
                "form": create_form
            }
            return render(request, 'users/register.html', context)


class LoginView(View):
    @staticmethod
    def get(request):
        login_form = AuthenticationForm()
        return render(request, 'users/login.html', {"login_form": login_form})

    @staticmethod
    def post(request):
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, "You have successfully logged in")
            return redirect("books:list")
        else:
            return render(request, 'users/login.html', {"login_form": login_form})


class ProfileView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        user = request.user
        return render(request, 'users/profile.html', {"user": user})


class ProfileUpdateView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        user_profile_form = ProfileUpdateForm(instance=request.user)
        return render(request, 'users/profile_edit.html', {"form": user_profile_form})

    @staticmethod
    def post(request):
        user_profile_form = ProfileUpdateForm(
            instance=request.user,
            data=request.POST,
            files=request.FILES
        )
        if user_profile_form.is_valid():
            user_profile_form.save()
            messages.success(request, "You have successfully updated your profile.")

            return redirect("users:profile")

        return render(request, 'users/profile_edit.html', {"form": user_profile_form})

class LogoutView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        logout(request)
        messages.info(request, "You have successfully logged out.")
        return redirect('home')
