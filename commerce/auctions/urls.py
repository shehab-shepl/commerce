from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watch_list, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("addcomment/<int:post_id>", views.add_comment, name="addcomment"),
    path("addbid/<int:post_id>", views.add_bid, name="addbid"),
    path("createlist", views.create_list, name="createlist"),
    path("<int:id>",views.post ,name='post')


]
