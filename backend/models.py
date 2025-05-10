import uuid
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Enum, Date, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import CHAR
from database import Base
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"

class User(Base):
    __tablename__ = "users"
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    buildings = relationship("Building", back_populates="owner")

class Building(Base):
    __tablename__ = "buildings"
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    address = Column(String(255), nullable=False)
    year_built = Column(Integer, nullable=False)
    cost_per_sqft = Column(Float, nullable=False)
    square_footage = Column(Float, nullable=False)
    image_url = Column(String(255))
    owner_id = Column(CHAR(36), ForeignKey("users.id"))
    owner = relationship("User", back_populates="buildings")
    pre_assessments = relationship("PreAssessment", back_populates="building")
    field_assessments = relationship("FieldAssessment", back_populates="building")

class BuildingTypeMapping(Base):
    __tablename__ = "building_type_mappings"
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    building_type = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    subcategory = Column(String(50), nullable=False)
    config = Column(JSON)

class PreAssessment(Base):
    __tablename__ = "pre_assessments"
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    building_id = Column(CHAR(36), ForeignKey("buildings.id"))
    date = Column(Date, nullable=False)
    items = relationship("PreAssessmentItem", back_populates="pre_assessment")
    building = relationship("Building", back_populates="pre_assessments")

class PreAssessmentItem(Base):
    __tablename__ = "pre_assessment_items"
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    pre_assessment_id = Column(CHAR(36), ForeignKey("pre_assessments.id"))
    category = Column(String(50), nullable=False)
    subcategory = Column(String(50), nullable=False)
    total_useful_life = Column(Integer, nullable=False)
    installation_year = Column(Integer, nullable=False)
    repair_frequency = Column(String(50), nullable=False)
    result = Column(String(50))
    pre_assessment = relationship("PreAssessment", back_populates="items")

class FieldAssessment(Base):
    __tablename__ = "field_assessments"
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    building_id = Column(CHAR(36), ForeignKey("buildings.id"))
    date = Column(Date, nullable=False)
    items = relationship("FieldAssessmentItem", back_populates="field_assessment")
    building = relationship("Building", back_populates="field_assessments")

class FieldAssessmentItem(Base):
    __tablename__ = "field_assessment_items"
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    field_assessment_id = Column(CHAR(36), ForeignKey("field_assessments.id"))
    category = Column(String(50), nullable=False)
    subcategory = Column(String(50), nullable=False)
    overall_result = Column(String(50), nullable=False)
    repair_cost = Column(Float)
    field_assessment = relationship("FieldAssessment", back_populates="items")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(CHAR(36), ForeignKey("users.id"))
    action = Column(String(255), nullable=False)
    timestamp = Column(Date, nullable=False)
    details = Column(Text)
