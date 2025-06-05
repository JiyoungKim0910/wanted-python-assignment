from sqlalchemy.orm import Session
from app.entity.models import Tag, TagName,CompanyTag

# tag 추가
def add_tag(name: str, language: str, db: Session ) -> Tag:
    # 추가할 Tag가 이미 존재하는지 확인
    tag = db.query(Tag).filter_by(language=language, name=name).first()
    if tag is None:
        # Tag 추가
        tag = Tag(language=language, name=name)
        db.add(tag)
    return tag

# 해당 회사에 tag 연결
def link_company_tag(company_id: int, tag_id: int, db: Session):
    db.add(CompanyTag(company_id=company_id, tag_id=tag_id))
    
# 태그명으로 회사 검색
def get_companies_by_tag(name: str, language: str,db: Session):
    return db.query(TagName).filter(TagName.language==language, TagName.name ==name).all()