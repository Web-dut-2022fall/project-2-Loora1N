from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:listId>", views.listing, name="listing"),
    path("listing/<int:listId>/watch", views.watch, name="watch"),
    path("watch", views.watchlist, name="watchlist"),
    path("listing/<int:listId>/bid", views.bid, name="bid"),
    path("close/<int:listId>", views.close, name="close"),
    path("comment/<int:listId>", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("category/<str:cateID>", views.category, name="category"),
]
