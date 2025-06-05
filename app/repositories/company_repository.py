from sqlalchemy.orm import Session
from app.entity.models import Company, CompanyName

# 회사명 일부로 검색
def get_companies_by_name_piece(query: str, db: Session):
    return db.query(CompanyName).filter(CompanyName.name.contains(query)).all()

# 회사명으로 회사 검색
def get_company_by_name(name: str, db: Session):
    return db.query(CompanyName).filter_by(name=name).all()