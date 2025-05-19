from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

class RedireccionPorRolMixin(LoginRequiredMixin):
    """
    Mixin que redirige al usuario si es staff a 'mensajeria:lista_alumnos'.
    Si no es staff, continúa con la vista normalmente.
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('mensajeria:lista_alumnos')
        return super().dispatch(request, *args, **kwargs)
