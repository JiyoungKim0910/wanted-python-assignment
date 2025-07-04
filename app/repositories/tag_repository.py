from sqlalchemy.orm import Session, joinedload
from app.entity.models import Tag, TagName,CompanyTag, Company

# tag 추가
def add_tag(name: str, language: str, tag: Tag, db: Session ) -> TagName:
    # 추가할 Tag가 이미 존재하는지 확인
    exist = db.query(TagName).filter_by(language=language, name=name).first()
    if exist is None:
        # Tag 추가
        tag_name = TagName(language=language, name=name, tag=tag)
        db.add(tag_name)
        db.flush()
        db.refresh(tag_name)
        return tag_name
    return exist

# 빈 태그 생성
def create_tag(db: Session):
    tag = Tag()
    db.add(tag)
    db.flush()
    db.refresh(tag)
    return tag

# 해당 회사에 tag 연결
def link_company_tag(company: Company, tag_id: int, db: Session):
    link = CompanyTag(company_id=company.id, tag_id=tag_id)
    db.add(link)
    db.flush()
    db.refresh(company)
    return company
    
# 태그명으로 회사 검색
def get_companies_by_tag(name: str, db: Session):
    return db.query(TagName).filter(TagName.name == name).all()
    
def unlink_company_tag(company: Company, tag_id: int, db: Session):
    # 회사와 연결 삭제
    db.query(CompanyTag).filter_by(company_id=company.id, tag_id=tag_id).delete()
    db.flush()
    db.refresh(company)
    
def get_count_tag_link(tag_id: int, db: Session):
    return db.query(CompanyTag).filter_by(tag_id=tag_id).count()

def delete_tag_name(tag_id: int, db: Session, company:Company):
    # TagName 삭제
    db.query(TagName).filter_by(tag_id=tag_id).delete()
    # Tag 삭제
    db.query(Tag).filter_by(id=tag_id).delete()
    db.flush()
    db.refresh(company)
    return company
    
    