import sys
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

sys.path.append("..")
from infrastructure.database import SessionLocal
from application import crud  
from domain.schemas import schemas
import fastapi_simple_security


empleados = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

depen = [Depends(fastapi_simple_security.api_key_security)]
emp = schemas.Empleado

@empleados.get("/empleados/", response_model=list[emp], dependencies=depen)
async def read_empleados(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    empleados = crud.get_empleados(db, skip=skip, limit=limit)

    return empleados


@empleados.get("/empleados/{empleado_id}", response_model=emp, dependencies=depen)
async def read_empleado(empleado_id: int, db: Session = Depends(get_db)):

    db_empleado = crud.get_empleado(db, empleado_id=empleado_id)

    if db_empleado is None:
        raise HTTPException(status_code=404, detail="No se encontro el Empleado")

    return db_empleado


@empleados.get("/empleados/{uuid_empleado}", response_model=emp, dependencies=depen)
async def read_empleado_uuid(uuid_empleado: str, db: Session = Depends(get_db)):

    db_empleado = crud.get_empleado_by_uuid(db, uuid_empleado)

    if db_empleado is None:
        raise HTTPException(status_code=404, detail="No se encontro el Empleado por el uuid")

    return db_empleado


@empleados.post("/empleados/", response_model=emp, dependencies=depen)
async def create_empleado(empleado: emp, db: Session = Depends(get_db)):

    db_empleado = crud.get_empleado_by_uuid(db, uuid=empleado.uuid)

    if db_empleado:
        raise HTTPException(status_code=400, detail="Empleado ya esta Registrado")

    return crud.create_empleado(db=db, empleado=dict(empleado))

@empleados.put("/empleados/{empleado_id}", dependencies=depen)
async def update_empleado(empleado_id: int,empleado: emp,db: Session = Depends(get_db)):

    db_empleado = crud.get_empleado(db, empleado_id=empleado_id)

    if db_empleado is None:
        raise HTTPException(status_code=404, detail="No se encontro el Empleado")

    try:
        crud.update_empleado(db=db,empleado_id=empleado_id,
                                empleado=dict(empleado))
        response = {"mensaje": "Se actualizo el empleado satisfactoriamente!",
                    "data": dict(empleado)}
    except:
        response = {"mensaje": "Error al actualizar el empleado"}
    
    return response


@empleados.delete("/empleados/{empleado_id}", dependencies=depen)
async def delete_empledo(empleado_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_empleado(db=db, empleado_id=empleado_id)
        response = {"mensaje": "Se elimino el empleado satisfactoriamente!"}
    except:
        response = {"mensaje": "Error al eleminar el empleado"}

    return response
