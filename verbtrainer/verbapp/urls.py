from django.urls import path
from .views import IrregularVerbListView, TrainerView, VerbUpdateView, AddVerbView

urlpatterns = [
    path('verb_list/', IrregularVerbListView.as_view(), name='verb_list'),
    path('trainer/', TrainerView.as_view(), name='trainer'),
    path('verb/<int:pk>/edit/', VerbUpdateView.as_view(), name='verb_edit'),
    path('verb/add/', AddVerbView.as_view(), name='verb_add'),
]