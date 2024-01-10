from django import forms
from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'description', 'ingredients', 'instructions']
        labels = {'title': 'Title', 'description': 'Description:', 'ingredients': 'Ingredients (Please add a comma between each ingredient):', 'instructions': 'Instructions (Please add a comma between each step):'}
    
