from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import TemplateView
from .forms import PostForm
from .models import New
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout


def home(request):
    data = {
        'news': New.objects.all(),
        'title': 'Агротехнологии'
    }
    return render(request, 'blog/home.html', data)


@login_required(login_url='/login/')
def contacts(request):
    return render(request, 'blog/contacts.html', {'title': 'Тренды агротехнологий'})


def add_post(request):
    return render(request, 'blog/post_edit.html', {'title': 'Добавить статью'})


def registration(request):
    form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'blog/home.html')


class RegisterView(TemplateView):
    template_name = "registration/register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            if password == password2:
                User.objects.create_user(username, email, password)
                return redirect("login")

        return render(request, self.template_name)


def post_detail(request, pk):
    post = get_object_or_404(New, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required(login_url='/login/')
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('/', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(New, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user,
            post.published_date = timezone.now()
            post.save()
            return redirect('/', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
