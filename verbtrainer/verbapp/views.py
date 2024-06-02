
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import ListView, View, UpdateView, CreateView

from .forms import TrainerForm, IrregularVerbForm
from .models import IrregularVerb


class IrregularVerbListView(ListView):
    queryset = IrregularVerb.objects.all().order_by('base')
    template_name = 'verbapp/verb_list.html'
    context_object_name = 'verbs'


class VerbUpdateView(UpdateView):
    model = IrregularVerb
    form_class = IrregularVerbForm
    template_name = 'verbapp/verb_edit.html'
    success_url = reverse_lazy('verb_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit'] = True
        return context


class AddVerbView(CreateView):
    model = IrregularVerb
    form_class = IrregularVerbForm
    template_name = 'verbapp/verb_add.html'
    success_url = reverse_lazy('verb_list')


class TrainerView(View):
    def get(self, request):
        task, guess_forms, translation = IrregularVerb.get_random_verb_as_task()
        form = TrainerForm(initial=task, editable_fields=guess_forms)
        return render(request, 'verbapp/trainer.html', {'form': form, 'translation': translation}, )

    def post(self, request, *args, **kwargs):
        form = TrainerForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            results, wrong_fields = IrregularVerb.objects.filter(id=id).first().check_forms(form.cleaned_data)
            form = TrainerForm(initial=results)
            return render(request, 'verbapp/trainer_result.html',
                          {'form': form, 'is_correct': len(wrong_fields) == 0,
                                   'wrong_fields': wrong_fields})
        else:
            return HttpResponse("Invalid form", status=400)
