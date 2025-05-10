from pydantic import BaseModel, EmailStr
from typing import Optional
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.user

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[UserRole] = None

class BuildingBase(BaseModel):
    name: str
    type: str
    city: str
    state: str
    address: str
    year_built: int
    cost_per_sqft: float
    square_footage: float
    image_url: Optional[str] = None

class BuildingCreate(BuildingBase):
    pass

class BuildingRead(BuildingBase):
    id: str
    owner_id: Optional[str] = None

class PreAssessmentItemBase(BaseModel):
    category: str
    subcategory: str
    total_useful_life: int
    installation_year: int
    repair_frequency: str
    result: Optional[str] = None

class PreAssessmentItemCreate(PreAssessmentItemBase):
    pass

class PreAssessmentItemUpdate(PreAssessmentItemBase):
    pass

class PreAssessmentItemRead(PreAssessmentItemBase):
    id: str
    pre_assessment_id: str

class FieldAssessmentItemBase(BaseModel):
    category: str
    subcategory: str
    overall_result: str
    repair_cost: Optional[float] = None

class FieldAssessmentItemCreate(FieldAssessmentItemBase):
    pass

class FieldAssessmentItemUpdate(FieldAssessmentItemBase):
    pass

class FieldAssessmentItemRead(FieldAssessmentItemBase):
    id: str
    field_assessment_id: str
