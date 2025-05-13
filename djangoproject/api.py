
from ninja_extra import NinjaExtraAPI
from apps.users.api_controller import AlumnosHookController
from apps.materias.api_controller import MateriasHookController
from apps.tareas.api_controller import TareasHookController
from apps.mensajeria.api_controller import MensajesHookController

api = NinjaExtraAPI()
api.register_controllers(AlumnosHookController)
api.register_controllers(MateriasHookController)
api.register_controllers(TareasHookController)
api.register_controllers(MensajesHookController)