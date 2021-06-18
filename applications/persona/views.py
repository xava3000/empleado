from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    TemplateView,
    UpdateView,
    DeleteView
)
from .models import Empleado

from .forms import EmpleadoForm


class InicioView(TemplateView):
    """ vista que carga la pagina de inicio"""
    template_name = "inicio.html"

class ListAllEmpleados(ListView):
    template_name = 'persona/list_all.html'
    paginate_by = 10
    ordering = 'first_name'
    context_object_name = 'empleados'

    def get_queryset(self):
        palabra_clave = self.request.GET.get("kword", '')
        lista = Empleado.objects.filter(
            full_name__icontains=palabra_clave
        )
        return lista


class ListaEmpleadosAdmin(ListView):
    template_name = 'persona/lista_empleados.html'
    paginate_by = 10
    ordering = 'first_name'
    context_object_name = 'empleados'
    model = Empleado


class ListByAreaEmpleado(ListView):
    """ Lista de los empleados por departamento """
    template_name = 'persona/list_by_area.html'
    context_object_name ='empleados'
    
    def get_queryset(self):
        area = self.kwargs['shorname']
        lista = Empleado.objects.filter(
            departamento__shor_name = area
        )
        return lista


class ListEmpleadosByKyword(ListView):
    """ Lista de empleados por palabra clave"""
    template_name = 'persona/by_kword.html'
    context_object_name = 'empleados'

    def get_queryset(self):
        print('*****************')
        palabra_clave = self.request.GET.get("kword", '')
        lista = Empleado.objects.filter(
            first_name = palabra_clave
        )
        print('lista resultado:', lista)
        return lista


class ListHabilidadesEmpleado(ListView):
    template_name = 'persona/habilidades.html'
    context_object_name = 'habilidades'
    
    def get_queryset(self):
        idempleado = self.request.GET.get("idempleado", '')
        empleado = Empleado.objects.get(id=str(idempleado))
        return empleado.habilidades.all()
# Lista de empleados por trabajo

# Detailview

class EmpleadoDetailView(DetailView):
    model = Empleado
    template_name = "persona/detail_empleado.html"

    def get_context_data(self, **kwargs):
        context = super(EmpleadoDetailView, self).get_context_data(**kwargs)
        context['titulo'] = 'Empleado del mes'
        return context


class SuccessView(TemplateView):
    template_name = "persona/success.html"


class EmpleadoCreateView(CreateView):
    model = Empleado
    template_name = "persona/add.html"
    form_class = EmpleadoForm
    #fields = ('__all__')
    success_url = reverse_lazy('persona_app:empleados_all')

    def form_valid(self, form):
        empleado = form.save(commit=False)
        empleado.full_name = empleado.first_name + ' ' + empleado.last_name
        empleado.save()
        return super(EmpleadoCreateView, self).form_valid(form)


class EmpleadoUpdateView(UpdateView):
    model = Empleado
    template_name = "persona/update.html"
    fields = [
        'first_name', 
        'last_name', 
        'job',
        'departamento',
        'habilidades'
    ]
    success_url = reverse_lazy('persona_app:empleados_admin')

    '''def post(self, request, *args, **kwargs):
    # Acceder a datos de la petición de HTML. 
    # Request es un diccionario con todos los datos
        self.object = self.get_object()
        print(request.POST['last_name'])
        return super(EmpleadoUpdateView).post(request, *args, **kwargs)
    
    def form_valid(self, form):
        return super(EmpleadoUpdateView, self).form_valid(form)
    '''

class EmpleadoDeleteView(DeleteView):
    model = Empleado
    template_name = "persona/delete.html"
    success_url = reverse_lazy('persona_app:empleados_admin')

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        print('===========================')
        print(request)
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)
