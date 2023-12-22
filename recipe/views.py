from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        # there's a line for Comments here - I'm leaving it out
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

class CreatePost(generic.CreateView):

    model = Post
    fields = ['title', 'content', 'ingredients', 'instructions']
    template_name = 'createpost.html'
    success_url = reverse_lazy('')