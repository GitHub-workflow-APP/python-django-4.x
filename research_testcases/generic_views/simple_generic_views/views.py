from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Person
from django.urls import reverse_lazy

class PersonCreate(CreateView):
    model = Person
    fields = '__all__'
    success_url = reverse_lazy('persons')

class PersonDetail(DetailView):
    model = Person 
    context_object_name = 'person'
    template_name = 'simple_generic_views/person.html'

class PersonList(ListView):
    model = Person
    context_object_name = 'persons'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['persons'] = context['persons'].filter(
                first_name__icontains=search_input)

        context['search_input'] = search_input

        return context

class PersonUpdate(UpdateView):
    model = Person 
    fields = '__all__'
    success_url = reverse_lazy('persons')


class DeleteView(DeleteView):
    model = Person 
    context_object_name = 'person'
    success_url = reverse_lazy('persons')
