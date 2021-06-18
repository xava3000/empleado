from django.shortcuts import render

# Create your views here.
from django.views.generic import (
    TemplateView, 
    ListView, 
    CreateView
)
from .models import Prueba

from .forms import PruebaForm

class PruebaView(TemplateView):
    template_name = 'home/prueba.html'

class ResumeFoundationView(TemplateView):
    template_name = 'home/resume_foundation.html'

class PruebaListView(ListView):
    template_name = "home/lista.html"
    context_object_name = 'ListaNumeros'
    queryset = ['0', '10', '20', '30']

class ListarPrueba(ListView):
    template_name = "home/lista_prueba.html"
    model = Prueba
    context_object_name = 'lista'


class PruebaCreateView(CreateView):
    model = Prueba
    template_name = "home/add.html"
    #fields = ['titulo', 'subtitulo','cantidad']
    form_class = PruebaForm
    success_url = '/'
