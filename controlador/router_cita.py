from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from servicio.cita_schema import CitaSchema
from config.db import engine
from modelo.citas import citas
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List
import doctest

cita= APIRouter()


@cita.post("/api/cita", status_code=HTTP_201_CREATED)
def create_cita(data_cita: CitaSchema):
    """
    los usuarios ingresa la cita con hora fecha que desea tener su cita medica 
    >>> create_cita("1","12-12-2023","10:30:00","A")
    """
    with engine.connect() as conn:
    
        new_cita = data_cita.dict()
    
        conn.execute(citas.insert().values(new_cita))

        return Response(status_code=HTTP_201_CREATED)
if __name__ == "__main__":
    doctest.testmod() 

@cita.put("/api/cita/{cita_id}", response_model=CitaSchema)
def update_cita(data_update: CitaSchema, cita_id: str):
    """
    la informacion de la reserva de la cita se actualiza por algun motivo del paciente 
    >>>update_cita("1","12-12-2023","11:00:00","A")
    """
    with engine.connect() as conn:
        conn.execute(citas.update().values(fecha=data_update.fecha, 
        hora=data_update.hora, estado=data_update.estado))

        result = conn.execute(citas.select().where(citas.c.id == cita_id)).first()

        return result
    

@cita.delete("/api/cita/{cita_id}", status_code=HTTP_204_NO_CONTENT)
def delete_cita(cita_id: str):
    """
    elimina la cita reservada del paciente o usuario
    >>>delete_user("","","","")
    """
    with engine.connect() as conn:
        conn.execute(cita.delete().where(cita.c.id == cita_id))

        return Response(status_code=HTTP_204_NO_CONTENT)