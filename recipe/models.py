from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


STATUS = ((0, "Draft"), (1, "Published"))


# Post model
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipe_posts")
    updated_on = models.DateTimeField(auto_now=True)
    featured_image = CloudinaryField('image', default='placeholder')
    description = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    favourites = models.ManyToManyField(User, related_name='recipe_favourites', blank=True)
    ingredients = models.TextField()
    instructions = models.TextField()

    class Meta:
        # in descending order by created on
        ordering = ['created_on']

    def __str__(self):
        return self.title

    def number_of_favourites(self):
        return self.favourites.count()

    @property
    def steps(self):
        return len(self.instructions.split(','))
