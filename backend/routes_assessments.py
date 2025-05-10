from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from models import PreAssessment, PreAssessmentItem, FieldAssessment, FieldAssessmentItem, Building
from schemas import BuildingRead
from auth import get_current_active_user

router = APIRouter(prefix="/assessments", tags=["assessments"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pre-Assessment Endpoints
@router.post("/pre/{building_id}")
def create_pre_assessment(building_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    building = db.query(Building).filter(Building.id == building_id).first()
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    pre = PreAssessment(building_id=building_id)
    db.add(pre)
    db.commit()
    db.refresh(pre)
    return pre

@router.get("/pre/{building_id}")
def get_pre_assessments(building_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    return db.query(PreAssessment).filter(PreAssessment.building_id == building_id).all()

# Field Assessment Endpoints
@router.post("/field/{building_id}")
def create_field_assessment(building_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    building = db.query(Building).filter(Building.id == building_id).first()
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    field = FieldAssessment(building_id=building_id)
    db.add(field)
    db.commit()
    db.refresh(field)
    return field

@router.get("/field/{building_id}")
def get_field_assessments(building_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    return db.query(FieldAssessment).filter(FieldAssessment.building_id == building_id).all()

@router.post("/field/{field_assessment_id}/calculate-fci")
def calculate_fci(field_assessment_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    field = db.query(FieldAssessment).filter(FieldAssessment.id == field_assessment_id).first()
    if not field:
        raise HTTPException(status_code=404, detail="FieldAssessment not found")
    building = db.query(Building).filter(Building.id == field.building_id).first()
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    items = db.query(FieldAssessmentItem).filter(FieldAssessmentItem.field_assessment_id == field_assessment_id).all()
    total_repair_cost = sum([item.repair_cost or 0 for item in items])
    replacement_cost = building.cost_per_sqft * building.square_footage
    fci = total_repair_cost / replacement_cost if replacement_cost else None
    return {"fci": fci, "total_repair_cost": total_repair_cost, "replacement_cost": replacement_cost}

@router.get("/field/{building_id}/report")
def field_assessment_report(building_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    fields = db.query(FieldAssessment).filter(FieldAssessment.building_id == building_id).all()
    report = []
    for field in fields:
        items = db.query(FieldAssessmentItem).filter(FieldAssessmentItem.field_assessment_id == field.id).all()
        total_repair_cost = sum([item.repair_cost or 0 for item in items])
        building = db.query(Building).filter(Building.id == building_id).first()
        replacement_cost = building.cost_per_sqft * building.square_footage if building else None
        fci = total_repair_cost / replacement_cost if replacement_cost else None
        report.append({
            "field_assessment_id": field.id,
            "date": field.date,
            "fci": fci,
            "total_repair_cost": total_repair_cost,
            "replacement_cost": replacement_cost
        })
    return report
