from django.urls import path

from management.views import UserAutocomplete


urlpatterns = [
    path("user-autocomplete/", UserAutocomplete.as_view(), name="user-autocomplete"),
]