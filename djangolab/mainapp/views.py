from django.shortcuts import render
from django.views.generic import FormView

from mainapp.models import Lab
from mainapp.forms import LabForm, DLabForm


class LabDetailView(FormView):

    form_class = DLabForm
    template_name = 'home.html'
    success_url = '2'

    def get_form_kwargs(self):
        form_kwargs = super(LabDetailView, self).get_form_kwargs()
        if 'pk' in self.kwargs:
            form_kwargs['instance'] = Lab.objects.get(pk=self.kwargs.get('pk'))
        return form_kwargs

    def form_valid(self, form):
        form.save()
        return super(LabDetailView, self).form_valid(form)

