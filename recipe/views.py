from django.shortcuts import render, get_object_or_404, redirect
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

def CreatePost(request):
    form = PostForm()
    if request.method == 'POST':
        print("working")
        field_form = PostForm(request.POST)
        if field_form.is_valid():
            recipe = Post()
            recipe.title = field_form.cleaned_data['title']
            recipe.slug = field_form.cleaned_data['title'].lower().replace(' ', '-')
            recipe.content = field_form.cleaned_data['content']
            recipe.ingredients = field_form.cleaned_data['ingredients']
            recipe.instructions = field_form.cleaned_data['instructions']
            recipe.author = User.objects.get(id = request.user.id)
            recipe.save()
            request.session['submit_success'] = 'Cocktail successfully submitted to the Admin for approval'
            return redirect('home')

    return render(request, 'createpost.html', {'form': form})

def Favourites(request):
    favourites = Post.objects.filter(favourites=request.user)
    return render(request, 'user.html', {'favourites': favourites})

def AddFavourites(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.favourites.add(request.user)
    return render(request, 'user.html')


# class CreatePost(LoginRequiredMixin, generic.CreateView):

#     model = Post
#     fields = ['title', 'content', 'ingredients', 'instructions']
#     template_name = 'createpost.html'
#     success_url = reverse_lazy('home')
#     login_url = '/login/'
#     # post = Post()
#     self.author_id = self.request.user

