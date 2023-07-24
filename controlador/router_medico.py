from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from servicio.medico_schema import MedicoSchema
from config.db import engine
from modelo.medico import medico
#from werkzeug.security import generate_password_hash, check_password_hash
from typing import List
import doctest

medico= APIRouter()

@medico.get("/")
def root():
    return{ "kevin"}

@medico.get("/api/medico", response_model=List[MedicoSchema])
def get_medico():
    with engine.connect() as conn:
        result = conn.execute(medico.select()).fetchall()
        return result
    
@medico.get("/api/medico/{medico_id}", response_model=MedicoSchema)
def get_medico(medico_id:str):
    with engine.connect() as conn:
        result = conn.execute(medico.select().where(medico.c.id == medico_id)).first()

        return result

@medico.post("/api/medico", status_code=HTTP_201_CREATED)
def create_medico(data_medico: MedicoSchema):
    """
    ingresa los datos de los medicos a la base de datos 
    >>> create_medico("1","kevin","mero","odontologo","123","123")
    """
    with engine.connect() as conn:
    
        new_medico = data_medico.dict()    
        conn.execute(medico.insert().values(new_medico))

        return Response(status_code=HTTP_201_CREATED)
if __name__ == "__main__":
    doctest.testmod()   

@medico.put("/api/medico/{medico_id}", response_model=MedicoSchema)
def update_medico(data_update: MedicoSchema, medico_id: str):
    """
    los datos de los usuario o paciente se actualiza si desea actualizar
    >>>update_medico("1","kevin","baque","odontologo","123445","123")
    """
    with engine.connect() as conn:
        conn.execute(medico.update().values(nombre=data_update.nombre, 
        apellido=data_update.apellido, especialidad=data_update.especialidad,
        cedula=data_update.cedula, telefono=data_update.telefono))

        result = conn.execute(medico.select().where(medico.c.id == medico_id)).first()

        return result
    

@medico.delete("/api/medico/{medico_id}", status_code=HTTP_204_NO_CONTENT)
def delete_medico(medico_id: str):
    """
    elimina todos los datos de un usuraio o paciente
    >>>delete_medico("","","","","","")
    """
    with engine.connect() as conn:
        conn.execute(medico.delete().where(medico.c.id == medico_id))

        return Response(status_code=HTTP_204_NO_CONTENT)