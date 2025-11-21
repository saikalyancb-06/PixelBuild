from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.database_models import Brand
from models.schemas import BrandCreate, BrandResponse

router = APIRouter()


@router.post("/", response_model=BrandResponse)
async def create_brand(brand: BrandCreate, db: Session = Depends(get_db)):
    """Register a new brand for protection"""
    db_brand = Brand(
        name=brand.name,
        package_ids=brand.package_ids,
        icon_urls=brand.icon_urls,
        developer_name=brand.developer_name,
        certificates=brand.certificates,
    )
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand


@router.get("/", response_model=List[BrandResponse])
async def list_brands(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all protected brands"""
    brands = db.query(Brand).offset(skip).limit(limit).all()
    return brands


@router.get("/{brand_id}", response_model=BrandResponse)
async def get_brand(brand_id: int, db: Session = Depends(get_db)):
    """Get a specific brand"""
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand
