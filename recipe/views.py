from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Home/index page - list of all cocktails
class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'


# View details of each cocktail
class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        favourited = False
        if post.favourites.filter(id=self.request.user.id).exists():
            favourited = True

        ingredients = post.ingredients
        ingredients = ingredients.split(',')
        i = 0
        while i < len(ingredients):
            ingredients[i] = ingredients[i].strip().strip('\t')
            i += 1

        instructions = post.instructions
        instructions = instructions.split(',')
        i = 0
        while i < len(instructions):
            instructions[i] = instructions[i].strip()
            i += 1

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "favourited": favourited,
                "ingredients": ingredients,
                "instructions": instructions,
            },
        )


# Cocktail submission form
@login_required
def CreatePost(request):
    form = PostForm()
    if request.method == 'POST':
        field_form = PostForm(request.POST)
        if field_form.is_valid():
            recipe = Post()
            recipe.title = field_form.cleaned_data['title']
            recipe.slug = field_form.cleaned_data['title'].lower().replace(' ', '-')
            recipe.description = field_form.cleaned_data['description']
            recipe.ingredients = field_form.cleaned_data['ingredients']
            recipe.instructions = field_form.cleaned_data['instructions']
            recipe.author = User.objects.get(id=request.user.id)
            recipe.save()
            messages.add_message(request, messages.INFO, 'Cocktail submitted to the Admin for approval')
            return redirect('home')

    return render(request, 'createpost.html', {'form': form})


@login_required
def Favourites(request):
    favourites = Post.objects.filter(favourites=request.user)
    return render(request, 'user.html', {'favourites': favourites})


# Adding/removing favourites
def AddFavourites(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.favourites.filter(id=request.user.id).count()==1:
        post.favourites.remove(request.user)
        messages.add_message(request, messages.INFO, 'You have unfavourited this cocktail')
    else:
        post.favourites.add(request.user)
        messages.add_message(request, messages.INFO, 'You have added this cocktail to your favourites')
    return redirect(request.META['HTTP_REFERER'])


# Error pages
def error_404_view(request, exception):
    """
    Displays 404.html path
    """
    return render(request, '404.html', status=404)


def handler500(request, *args, **argv):
    """
    Displays 500.html path
    """
    return render(request, '500.html', status=500)


def handler403(request, *args, **argv):
    """
    Displays 403.html path
    """
    return render(request, '403.html', status=403)


# Search functionality
def SearchIngredient(request):
    if  'searchstring' in request.POST:
        searchstring = request.POST['searchstring']
        search = Post.objects.filter(ingredients__icontains=searchstring)
        if len(search)==0:
            messages.add_message(request, messages.INFO, 'No cocktail with that ingredient')
            return redirect('home')
    else:
        return redirect('home')
    return render(request, 'search.html', {'search': search})


# Delete functionality
def DeletePost(request, slug):
    if  request.method=='POST':
        cocktail = Post.objects.get(slug=slug)
        cocktail.delete()
        messages.add_message(request, messages.INFO, 'Cocktail deleted successfully')
        return redirect('home')
    else:
        cocktail = Post.objects.get(slug=slug)
        return render(request, 'delete.html', {'cocktail': cocktail})


# Update functionality
def UpdatePost(request, slug):
    form = PostForm()
    if request.method == 'POST':
        description = request.POST['description']
        ingredients = request.POST['ingredients']
        instructions = request.POST['instructions']
        Post.objects.update_or_create(slug=slug, defaults={'description': description, 'ingredients': ingredients, 'instructions': instructions})
        messages.add_message(request, messages.INFO, 'Update successfully completed')
        return redirect('home')

    cocktail = Post.objects.get(slug=slug)

    return render(request, 'update.html', {'form': form, 'cocktail': cocktail})
