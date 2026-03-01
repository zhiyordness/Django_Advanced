from django.urls import path

from notes import views

urlpatterns = [
    path('', views.NoteListView.as_view(), name='list'),
    path('<int:pk>/', views.NoteDetailView.as_view(), name='detail'),
]