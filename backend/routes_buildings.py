from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from models import Building
from schemas import BuildingCreate, BuildingRead
from auth import get_current_active_user

router = APIRouter(prefix="/buildings", tags=["buildings"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from models import AuditLog
from datetime import date

@router.post("/", response_model=BuildingRead, status_code=status.HTTP_201_CREATED)
def create_building(building: BuildingCreate, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    db_building = Building(**building.dict(), owner_id=current_user.id)
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    db.add(AuditLog(user_id=current_user.id, action="create_building", timestamp=date.today(), details=f"Created building {db_building.id}"))
    db.commit()
    return db_building

from fastapi import Query

@router.get("/", response_model=List[BuildingRead])
def list_buildings(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    city: str = Query(None),
    state: str = Query(None),
    type: str = Query(None),
    search: str = Query(None),
    sort: str = Query("name"),
    order: str = Query("asc")
):
    q = db.query(Building)
    if city:
        q = q.filter(Building.city.ilike(f"%{city}%"))
    if state:
        q = q.filter(Building.state.ilike(f"%{state}%"))
    if type:
        q = q.filter(Building.type.ilike(f"%{type}%"))
    if search:
        q = q.filter(
            (Building.name.ilike(f"%{search}%")) |
            (Building.address.ilike(f"%{search}%"))
        )
    if hasattr(Building, sort):
        sort_col = getattr(Building, sort)
        q = q.order_by(sort_col.desc() if order == "desc" else sort_col.asc())
    return q.all()

@router.get("/{building_id}", response_model=BuildingRead)
def get_building(building_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    building = db.query(Building).filter(Building.id == building_id).first()
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return building

from models import AuditLog
from datetime import date

@router.put("/{building_id}", response_model=BuildingRead)
def update_building(building_id: str, building: BuildingCreate, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    db_building = db.query(Building).filter(Building.id == building_id).first()
    if not db_building:
        raise HTTPException(status_code=404, detail="Building not found")
    for key, value in building.dict().items():
        setattr(db_building, key, value)
    db.commit()
    db.refresh(db_building)
    db.add(AuditLog(user_id=current_user.id, action="update_building", timestamp=date.today(), details=f"Updated building {building_id}"))
    db.commit()
    return db_building

from auth import get_admin_user
from models import AuditLog
from datetime import date

@router.delete("/{building_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_building(building_id: str, db: Session = Depends(get_db), current_user=Depends(get_admin_user)):
    db_building = db.query(Building).filter(Building.id == building_id).first()
    if not db_building:
        raise HTTPException(status_code=404, detail="Building not found")
    db.delete(db_building)
    db.add(AuditLog(user_id=current_user.id, action="delete_building", timestamp=date.today(), details=f"Deleted building {building_id}"))
    db.commit()
    return None
