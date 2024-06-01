from django.shortcuts import render
from django.contrib.auth import get_user_model

from dal import autocomplete


class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        User = get_user_model()
        # Don't forget to filter out results depending on the visitor !

        qs = User.objects.all()

        if self.q:
            qs = qs.filter(phone_number__istartswith=self.q)

        return qs
