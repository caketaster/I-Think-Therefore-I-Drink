"""thinkdrink URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from recipe import views
from django.conf.urls import handler403, handler404, handler500

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('recipe/', include('recipe.urls'), name='recipe_urls'),
    path('accounts/', include('allauth.urls')),
    path('submitcocktail/', views.CreatePost, name='submitcocktail'),
    path('favourites/', views.Favourites, name='favourites'),
    path('addfavourites/<int:post_id>/', views.AddFavourites, name='addfavourites'),  # noqa
    path('search/', views.SearchIngredient, name='search')
]

handler403 = 'recipe.views.handler403'
handler404 = 'recipe.views.error_404_view'
handler500 = 'recipe.views.handler500'
