# api/hooks/schemas.py
from ninja import Schema
from typing import Optional

class TareaCrearHookIn(Schema):
    tareaid: int
    cmid: int
    courseid: int
    nombre: str  # Puedes agregar más campos si los necesitas
    
class TareaCalificarHookIn(Schema):
    tareaid: Optional[int] = None
    userid: Optional[int] = None
    nombre: Optional[str] = None
    cmid: Optional[int] = None
    courseid: Optional[int] = None
