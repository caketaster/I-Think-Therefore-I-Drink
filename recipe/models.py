from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


STATUS = ((0, "Draft"), (1, "Published"))


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    # n.b. recipe_posts not blog_posts
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipe_posts")
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    # changed from 'excerpt'
    description = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    # n.b. favourites not 'likes' (integer?)
    favourites = models.ManyToManyField(User, related_name='recipe_favourites', blank=True)
    # n.b. ingredients is a list. not sure how to do this - CharField? required/blank=False
    ingredients = models.CharField(max_length=800)
    # n.b. instructions is obvs new
    instructions = models.CharField(max_length=800)

    class Meta:
        # in descending order by created on - might change this ordering
        ordering = ['created_on']

    # a 'magic method' that returns a string representation of an object. You should define it because the default isn't helpful at all(!)
    def __str__(self):
        return self.title

    # n.b. in the walkthrough this is number_of_likes
    def number_of_favourites(self):
        return self.favourites.count()


class Submit_form(models.Model):
    # n.b. renamed author/related_name, removed favourites
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    # n.b. submit_posts not blog_posts
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submit_posts")
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    # changed from 'excerpt'
    # delete description / merge with content
    description = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    # n.b. ingredients is an unordered list. not sure how to do this - CharField? required/blank=False
    ingredients = models.CharField(max_length=800)
    # n.b. instructions is obvs new (needs to be ordered list)
    instructions = models.CharField(max_length=800)
    # n.b. do I need an 'approved' field? Copied from ITTIB here:
    approved = models.BooleanField(default=False)
    email = models.EmailField(null=True, blank=True)
    class Meta:
        # in descending order by created on - might change this ordering
        ordering = ['-created_on']

    # a 'magic method' that returns a string representation of an object. You should define it because the default isn't helpful at all(!)
    def __str__(self):
        return self.title

    
# # I'm not having comments, I'm having recipe submissions. Will comment this out until I can create the submission form and replace it
# class Comment(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
#     name = models.CharField(max_length=80)
#     email = models.EmailField()
#     body = models.TextField()
#     created_on = models.DateTimeField(auto_now_add=True)
#     approved = models.BooleanField(default=False)

#     class Meta:
#         # in ascending order by created on - might change this ordering
#         ordering = ['created_on']

#     # a 'magic method' that returns a string representation of an object. You should define it because the default isn't helpful at all(!)
#     def __str__(self):
#         return f"Comment {self.body} by {self.name}"