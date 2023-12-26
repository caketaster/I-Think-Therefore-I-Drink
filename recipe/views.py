from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        favourited = False
        if post.favourites.filter(id=self.request.user.id).exists():
            favourited = True
        # n.b. 'favourited' not 'liked'

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "favourited": favourited,
            },
        )

# start from here - make function based
class CreatePost(LoginRequiredMixin, generic.CreateView):

    model = Post
    fields = ['title', 'content', 'ingredients', 'instructions']
    template_name = 'createpost.html'
    success_url = reverse_lazy('home')
    login_url = '/login/'
    # post = Post()
    self.author_id = self.request.user