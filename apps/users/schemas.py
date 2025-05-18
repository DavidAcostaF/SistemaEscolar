# api/hooks/schemas.py
from ninja import Schema

class AlumnoHookIn(Schema):
    userid: int
    