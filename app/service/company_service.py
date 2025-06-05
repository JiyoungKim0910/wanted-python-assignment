from sqlalchemy.orm import Session
from app.entity.models import Company, CompanyName, Tag, TagName, CompanyTag
from app.schemas import TagUpdateSchema
from typing import List


# 다국어 데이터 목록에서 요청된 언어 데이터가 있으면 반환
def get_localized(items, language):
    lang_map = {items.language: item.name for item in items}
    return lang_map.get(language) or next(iter(lang_map.values()), None)

# 회사명으로 회사찾기
def find_company_by_name(name, db:Session):
    return db.query(Company).join(CompanyName).filter(CompanyName.name == name).first()

# 회사명 자동 완성
def search_company_autocomplete(query: str, lang: str, db: Session):
    
    names = db.query(CompanyName).filter(CompanyName.name.contains(query)).all()
    
    # 중복 제거
    x, result = set(), []
    for name in names:
        company_name = get_localized(name.company.names, lang)
        if company_name not in x:
            result.append({"company_name":company_name})
            x.add(company_name)
        
    return result

# 회사명으로 회사 검색        
def get_company_by_name(name: str, lang: str, db: Session):
    company = find_company_by_name(name, db)
    if not company:
        raise Exception("Company not found")
    company_name = get_localized(company.names, lang)
    tags = [get_localized(ct.tag.names, lang) for ct in company.tags]
    return {"company_name":company_name, "tags": sorted(set(tags))}

#search_by_tag
#add_tags
#delete_tag