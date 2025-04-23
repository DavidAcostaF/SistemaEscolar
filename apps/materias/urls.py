from django.urls import path
from .views import  MateriasView, DetalleMateriaView

app_name = 'materias'

urlpatterns = [
    path('materias/', MateriasView.as_view(), name='materias'),
    # path('', ListaMateriasView.as_view(), name='lista_materias'),
    path('detalle/<int:curso_id>/', DetalleMateriaView.as_view(), name='detalle_materia'),
]
