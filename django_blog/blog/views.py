from django.db.models import Q
from taggit.models import Tag

from .models import Comment
from .forms import CommentForm

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)

from .models import Post
from .forms import PostForm


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegisterForm, ProfileForm


# LOGIN
def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('profile')

        else:
            messages.error(request, "Invalid username or password")


    return render(request, "blog/login.html")


# LOGOUT
def user_logout(request):
    logout(request)
    return redirect('login')


# REGISTER
def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect('login')

    else:
        form = RegisterForm()

    return render(
        request,
        "blog/register.html",
        {"form": form}
    )


#SEARCH RESULTS
def search_results(request):
    query = request.GET.get('q')
    results = Post.objects.none()
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    context = {'results': results, 'query': query}
    return render(request, 'blog/search_results.html', context)


# TAG FILTER
def posts_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags__in=[tag])
    context = {'posts': posts, 'tag': tag}
    return render(request, 'blog/tag_posts.html', context)


# PROFILE
@login_required
def profile(request):

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated")

    else:
        form = ProfileForm(instance=request.user)


    return render(
        request,
        "blog/profile.html",
        {"form": form}
    )



# -----------------------------
# BLOG POST CRUD VIEWS
# -----------------------------


class PostListView(ListView):

    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']


class PostDetailView(DetailView):

    model = Post
    template_name = 'blog/post_detail.html'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['comments'] = self.object.comments.all()

        return context



class PostCreateView(LoginRequiredMixin, CreateView):

    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):

        form.instance.author = self.request.user

        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):

        form.instance.author = self.request.user

        return super().form_valid(form)


    def test_func(self):

        post = self.get_object()

        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/posts/'

    def test_func(self):

        post = self.get_object()

        return self.request.user == post.author



class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/tag_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        return Post.objects.filter(tags__slug=tag_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get('tag_slug')
        context['tag'] = get_object_or_404(Tag, slug=tag_slug)
        return context
    
    
# -----------------------------
# COMMENT VIEWS
# -----------------------------


class CommentCreateView(LoginRequiredMixin, CreateView):

    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'


    def form_valid(self, form):

        post = Post.objects.get(pk=self.kwargs['pk'])

        form.instance.post = post
        form.instance.author = self.request.user

        return super().form_valid(form)


    def get_success_url(self):

        return self.object.post.get_absolute_url()



class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'


    def test_func(self):

        comment = self.get_object()

        return self.request.user == comment.author


    def get_success_url(self):

        return self.object.post.get_absolute_url()



class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Comment
    template_name = 'blog/comment_confirm_delete.html'


    def test_func(self):

        comment = self.get_object()

        return self.request.user == comment.author


    def get_success_url(self):

        return self.object.post.get_absolute_url()
