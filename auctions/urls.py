from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/<int:listing_id>/bid", views.bid, name="bid"),
    path("listing/<int:listing_id>/close_listing", views.close_listing, name="close_listing"),
    path("listing/<int:listing_id>/comment", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_name>", views.category, name="category"),
    path("create_listing", views.create, name="create_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_watchlist/<int:listing_id>", views.addWatchlist, name="add_watchlist"),
    path("remove_watchlist/<int:listing_id>", views.removeWatchlist, name="remove_watchlist"),
]
