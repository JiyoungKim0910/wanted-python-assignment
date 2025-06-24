from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException
from app.entity.models import Company
from app.repositories import company_repository, tag_repository
from app.schemas import CompanyCreateSchema, TagUpdateSchema, CompanyResponseSchema, CompanyNameSchema
from app.utils.localization import get_localized, get_localized_strict
from app.utils.db_transaction import transactional

# 회사명 자동 완성
def search_company_autocomplete(query: str, lang: str, db: Session):
    
    c_names = company_repository.get_companies_by_name_piece(query,db)
    
    # 중복 제거
    exist, result = set(), []
    for name in c_names:
        company_name = get_localized(name.company.company_name, lang)
        if company_name not in exist:
            result.append(CompanyNameSchema(company_name=company_name))
            exist.add(company_name)
        
    return result

# 회사명으로 회사 검색        
def get_company_by_name(name: str, lang: str, db: Session):
    company = company_repository.get_company_by_name(name, db)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    company_name = get_localized(company.company_name, lang)
    localized_tags = []
    for ct in company.tags:
        name = get_localized_strict(ct.tag.tag_names, lang)
        if name:
            localized_tags.append(name)
    unique_tags = sorted(localized_tags,key=lambda x: int(x.split("_")[1]))
    return CompanyResponseSchema(company_name=company_name,tags=unique_tags)


# 회사 추가
@transactional
def create_company(data: CompanyCreateSchema, lang:str, db: Session):
    company = company_repository.create_company(db)
    
    for l, name in data.company_name.items():
        company_repository.add_company_name(company, l, name, db)
        
    c_name = get_localized(company.company_name, lang)
    
    return add_tags(c_name, data.tags, lang, db=db)
    

    
# 태그명으로 회사 검색
def search_by_tag(tag_name: str, lang: str, db: Session):
    tags =  tag_repository.get_companies_by_tag(tag_name, db)
    exist, result = set(), []
    if not tags:
        raise HTTPException(status_code=404, detail="Tag not found")
    for tag_name in tags:
        tag = tag_name.tag
        for ct in tag.company_tags:
            company = ct.company
            if company.id in exist:
                continue
            exist.add(company.id)
            company_name =  get_localized(company.company_name, lang)
            result.append(CompanyNameSchema(company_name=company_name))
            
    return result

# 태그 추가
@transactional
def add_tags(name: str, tags: List[TagUpdateSchema], lang: str, db: Session):
    company = company_repository.get_company_by_name(name, db)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    for tag_data in tags:
        # 새 태그 생성
        c_tag = tag_repository.create_tag(db)
        for l, tagname in tag_data.tag_name.items():
            # 다국어 TagName 추가
            tag = tag_repository.add_tag(tagname,l,c_tag,db)
        tag_repository.link_company_tag(company, c_tag.id, db)
    
    c_name = get_localized(company.company_name, lang)
    localized_tags = []
    for ct in company.tags:
        name = get_localized_strict(ct.tag.tag_names, lang)
        if name:
            localized_tags.append(name)
    unique_tags = sorted(localized_tags,key=lambda x: int(x.split("_")[1]))
    return CompanyResponseSchema(company_name=c_name,tags=unique_tags)
        
# 태그 삭제
@transactional
def delete_tag(name: str, tag_name: str, lang: str, db: Session):
    company = company_repository.get_company_by_name(name, db)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    tags = tag_repository.get_companies_by_tag(tag_name,db)
    if not tags:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    tag_id = tags[0].tag_id
    
    # 회사랑 태그연결 해제
    tag_repository.unlink_company_tag(company,tag_id,db)
    
    #해당 태그가 더 이상 어떤 회사와도 연결되어 있지 않다면
    #Tag가 Orphan 될 수 있으므로 태그명도 삭제
    remaining_links = tag_repository.get_count_tag_link(tag_id,db)
    if remaining_links == 0:
        tag_repository.delete_tag_name(tag_id, db,company)
    
    c_name = get_localized(company.company_name, lang)
    localized_tags = []
    for ct in company.tags:
        name = get_localized_strict(ct.tag.tag_names, lang)
        if name:
            localized_tags.append(name)
    unique_tags = sorted(localized_tags,key=lambda x: int(x.split("_")[1]))
    return CompanyResponseSchema(company_name=c_name,tags=unique_tags)