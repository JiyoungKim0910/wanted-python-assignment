from sqlalchemy.orm import Session
from typing import List

from app.repositories import company_repository, tag_repository
from app.schemas import CompanyCreateSchema, TagUpdateSchema
from app.utils.localization import get_localized, get_localized_strict


# 회사명 자동 완성
def search_company_autocomplete(query: str, lang: str, db: Session):
    
    c_names = company_repository.get_companies_by_name_piece(query,db)
    
    # 중복 제거
    x, result = set(), []
    for name in c_names:
        company_name = get_localized(name.company.company_name, lang)
        if company_name not in x:
            result.append({"company_name":company_name})
            x.add(company_name)
        
    return result

# 회사명으로 회사 검색        
def get_company_by_name(name: str, lang: str, db: Session):
    company = company_repository.get_company_by_name(name, db)
    if not company:
        raise Exception("Company not found")
    company_name = get_localized(company.company_name, lang)
    localized_tags = []
    for ct in company.tags:
        name = get_localized_strict(ct.tag.tag_names, lang)
        if name:
            localized_tags.append(name)
    unique_tags = sorted(set(localized_tags))
    return {"company_name":company_name, "tags": unique_tags}


# 회사 추가
def create_company(data: CompanyCreateSchema, lang:str, db: Session):
    company = company_repository.create_company(db)
    
    for lang, name in data.company_name.items():
        company_repository.add_company_name(company, lang, name, db)
        db.flush()
    db.commit()
    db.refresh(company)
    c_name = get_localized(company.company_name, lang)
    return add_tags(c_name, data.tags, lang, db)
    

    
# 태그명으로 회사 검색
def search_by_tag(tag_name: str, lang: str, db: Session):
    tags =  tag_repository.get_companies_by_tag(tag_name, db)
    x, result = set(), []
    if not tags:
        raise Exception("Tag not found")
    for tag_name in tags:
        tag = tag_name.tag
        for ct in tag.company_tags:
            company = ct.company
            if company.id in x:
                continue
            x.add(company.id)
            result.append(get_localized(company.company_name, lang))
    return result

# 태그 추가
def add_tags(name: str, tags: List[TagUpdateSchema], lang: str, db: Session):
    company = company_repository.get_company_by_name(name, db)
    if not company:
        raise Exception("Company not found")
    
    for tag_data in tags:
        # 새 태그 생성
        c_tag = tag_repository.create_tag(db)
        for l, tagname in tag_data.tag_name.items():
            # 다국어 TagName 추가
            tag = tag_repository.add_tag(tagname,l,c_tag,db)
        tag_repository.link_company_tag(company.id, c_tag.id, db)
        db.flush()
    db.commit()
    db.refresh(company)
    cname = get_localized(company.company_name, lang)
    localized_tags = []
    for ct in company.tags:
        name = get_localized(ct.tag.tag_names, lang)
        if name:
            localized_tags.append(name)
    unique_tags = sorted(set(localized_tags))
    return {"company_name": cname, "tags": unique_tags}
        
#delete_tag