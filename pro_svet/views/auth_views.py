"""
Authentication views for the Prosvet application.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User
from pro_svet.models import UserProfile


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('profile')  # Redirect to profile after login

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        messages.success(self.request, f'Добро пожаловать, {form.get_user().username}!')
        return super().form_valid(form)


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Basic validation
        if password1 != password2:
            messages.error(request, 'Пароли не совпадают.')
            return render(request, 'registration/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Имя пользователя уже занято.')
            return render(request, 'registration/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email уже используется.')
            return render(request, 'registration/register.html')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        # Create user profile
        UserProfile.objects.create(user=user)

        # Authenticate and login
        user = authenticate(
            request,
            username=username,
            password=password1
        )
        if user is not None:
            login(request, user)
            messages.success(request, 'Регистрация успешна! Добро пожаловать!')
            return redirect('profile')

    return render(request, 'registration/register.html')