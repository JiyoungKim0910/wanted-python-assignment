from sqlalchemy.orm import Session
from app.entity.models import Company, CompanyName

# 회사명 일부로 검색
def get_companies_by_name_piece(query: str, db: Session):
    return db.query(CompanyName).filter(CompanyName.name.contains(query)).all()

# 회사명으로 회사 검색
def get_company_by_name(name: str, db: Session):
    company = db.query(CompanyName).filter_by(name=name).first()
    if company:
        return company.company
    return None

# 회사 등록
def create_company(db: Session) -> Company:
    company = Company()
    db.add(company)
    db.flush()
    return company

# 회사 이름 추가
def add_company_name(company: Company, language: str, name: str, db: Session):
    db.add(CompanyName(company=company, language=language, name=name))
    
