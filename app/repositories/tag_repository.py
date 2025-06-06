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
        return tag_name
    return exist

# 빈 태그 생성
def create_tag(db: Session):
    tag = Tag()
    db.add(tag)
    db.flush()
    return tag

# 해당 회사에 tag 연결
def link_company_tag(company_id: int, tag_id: int, db: Session):
    db.add(CompanyTag(company_id=company_id, tag_id=tag_id))
    
# 태그명으로 회사 검색
def get_companies_by_tag(name: str, db: Session):
    return (db.query(TagName)
    .options(
        joinedload(TagName.tag)
        .joinedload(Tag.company_tags)
        .joinedload(CompanyTag.company)
        .joinedload(Company.company_name)
    )
    .filter(TagName.name == name).all())