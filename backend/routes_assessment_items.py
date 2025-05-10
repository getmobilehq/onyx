from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from models import PreAssessmentItem, FieldAssessmentItem, PreAssessment, FieldAssessment, AuditLog
from schemas import (
    PreAssessmentItemCreate, PreAssessmentItemUpdate, PreAssessmentItemRead,
    FieldAssessmentItemCreate, FieldAssessmentItemUpdate, FieldAssessmentItemRead
)
from auth import get_current_active_user, get_admin_user
from datetime import date

router = APIRouter(prefix="/assessment-items", tags=["assessment-items"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- PreAssessmentItem CRUD ---
@router.post("/pre/{pre_assessment_id}", response_model=PreAssessmentItemRead, status_code=status.HTTP_201_CREATED)
def create_pre_item(pre_assessment_id: str, item: PreAssessmentItemCreate, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    pre = db.query(PreAssessment).filter(PreAssessment.id == pre_assessment_id).first()
    if not pre:
        raise HTTPException(status_code=404, detail="PreAssessment not found")
    db_item = PreAssessmentItem(**item.dict(), pre_assessment_id=pre_assessment_id)
    db.add(db_item)
    db.add(AuditLog(user_id=current_user.id, action="create_pre_assessment_item", timestamp=date.today(), details=f"PreAssessmentItem {db_item.id}"))
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/pre/{pre_assessment_id}", response_model=List[PreAssessmentItemRead])
def list_pre_items(pre_assessment_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    return db.query(PreAssessmentItem).filter(PreAssessmentItem.pre_assessment_id == pre_assessment_id).all()

@router.put("/pre/{item_id}", response_model=PreAssessmentItemRead)
def update_pre_item(item_id: str, item: PreAssessmentItemUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    db_item = db.query(PreAssessmentItem).filter(PreAssessmentItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.add(AuditLog(user_id=current_user.id, action="update_pre_assessment_item", timestamp=date.today(), details=f"PreAssessmentItem {item_id}"))
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/pre/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pre_item(item_id: str, db: Session = Depends(get_db), current_user=Depends(get_admin_user)):
    db_item = db.query(PreAssessmentItem).filter(PreAssessmentItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.add(AuditLog(user_id=current_user.id, action="delete_pre_assessment_item", timestamp=date.today(), details=f"PreAssessmentItem {item_id}"))
    db.commit()
    return None

# --- FieldAssessmentItem CRUD ---
@router.post("/field/{field_assessment_id}", response_model=FieldAssessmentItemRead, status_code=status.HTTP_201_CREATED)
def create_field_item(field_assessment_id: str, item: FieldAssessmentItemCreate, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    field = db.query(FieldAssessment).filter(FieldAssessment.id == field_assessment_id).first()
    if not field:
        raise HTTPException(status_code=404, detail="FieldAssessment not found")
    db_item = FieldAssessmentItem(**item.dict(), field_assessment_id=field_assessment_id)
    db.add(db_item)
    db.add(AuditLog(user_id=current_user.id, action="create_field_assessment_item", timestamp=date.today(), details=f"FieldAssessmentItem {db_item.id}"))
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/field/{field_assessment_id}", response_model=List[FieldAssessmentItemRead])
def list_field_items(field_assessment_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    return db.query(FieldAssessmentItem).filter(FieldAssessmentItem.field_assessment_id == field_assessment_id).all()

@router.put("/field/{item_id}", response_model=FieldAssessmentItemRead)
def update_field_item(item_id: str, item: FieldAssessmentItemUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    db_item = db.query(FieldAssessmentItem).filter(FieldAssessmentItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.add(AuditLog(user_id=current_user.id, action="update_field_assessment_item", timestamp=date.today(), details=f"FieldAssessmentItem {item_id}"))
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/field/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_field_item(item_id: str, db: Session = Depends(get_db), current_user=Depends(get_admin_user)):
    db_item = db.query(FieldAssessmentItem).filter(FieldAssessmentItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.add(AuditLog(user_id=current_user.id, action="delete_field_assessment_item", timestamp=date.today(), details=f"FieldAssessmentItem {item_id}"))
    db.commit()
    return None
