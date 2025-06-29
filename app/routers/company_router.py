from fastapi import APIRouter, Depends, Header, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.entity.models import Company, CompanyName, Tag, TagName, CompanyTag
from app.schemas import CompanyResponseSchema, TagNameSchema, TagUpdateSchema ,CompanyCreateSchema, CompanyNameSchema
from app.service import company_service

router = APIRouter()

def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close
    
    
@router.get("/search", response_model=List[CompanyNameSchema], summary="회사명 자동완성" , tags=["Company"])
def autocomplete_company(
    query: str = Query(..., description="회사명 일부"),
    x_wanted_language: str = Header("ko"),
    db: Session = Depends(get_db)
):
    return company_service.search_company_autocomplete(query=query, lang=x_wanted_language, db=db)

@router.get("/companies/{name}", response_model=CompanyResponseSchema, summary="회사명 검색", tags=["Company"])
def get_company(
    name: str ,
    x_wanted_language: str = Header("ko"),
    db: Session = Depends(get_db)
):
    return company_service.get_company_by_name(name=name, lang=x_wanted_language, db=db)

@router.post("/companies", response_model=CompanyResponseSchema, summary="회사 등록", tags=["Company"])
def create_company(
    body: CompanyCreateSchema,
    x_wanted_language: str = Header("ko"),
    db: Session = Depends(get_db)
):
    return company_service.create_company(data=body, lang=x_wanted_language, db=db)


@router.get("/tags", response_model=List[CompanyNameSchema] , summary="태그명으로 회사 검색", tags=["Tag"])
def get_company_by_tag(
    query: str = Query(..., description="태그명"),
    x_wanted_language: str = Header("ko"),
    db: Session = Depends(get_db)
):
    return company_service.search_by_tag(tag_name=query, lang=x_wanted_language, db=db)

@router.put("/companies/{name}/tags", response_model=CompanyResponseSchema, summary="회사 태그 정보 추가", tags=["Tag"])
def add_tag_to_company(
    name: str ,
    tags: List[TagUpdateSchema],
    x_wanted_language: str = Header("ko"),
    db: Session = Depends(get_db)
):
    return company_service.add_tags(name=name, tags=tags, lang=x_wanted_language, db=db)

@router.delete("/companies/{name}/tags/{tagname}", response_model=CompanyResponseSchema, summary="회사 태그 정보 삭제", tags=["Tag"])
def delete_tag(
    name: str,
    tagname: str,
    x_wanted_language: str = Header("ko"),
    db: Session = Depends(get_db)
):
    return company_service.delete_tag(name=name, tag_name=tagname, lang=x_wanted_language, db=db)


