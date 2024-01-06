from . import views
from django.urls import path


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('<slug:slug>/delete/', views.DeletePost, name='delete'),
    path('<slug:slug>/update/', views.UpdatePost, name='update'),
] 