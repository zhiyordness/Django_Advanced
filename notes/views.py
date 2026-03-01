from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from notes.models import Note


# Create your views here.

class NoteListView(LoginRequiredMixin, ListView):
    model = Note

    def get_queryset(self):
        qs = Note.objects.select_related('owner')
        if not self.request.user.has_perm('can_access_all_notes'):
            return qs.filter(owner=self.request.user)

        return qs


class NoteDetailView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    queryset = Note.objects.select_related('owner')

    def test_func(self):
        return (
            self.request.user.has_perm('notes.can_access_all_notes') or
            self.get_object().owner == self.request.user
        )