import csv
import os
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.entity.models import Base, Company, CompanyName, Tag, TagName, CompanyTag

# 테이블이 없으면 자동 생성
Base.metadata.create_all(bind=engine)

def load_csv_to_db(file_path: str):
    db: Session = SessionLocal()
    
    # 이미 DB에 데이터가 로드됐는지 체크
    if db.query(Company).first():
        print("Sample data already loaded.")
        db.close()
        return
    
    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            company = Company()
            db.add(company)
            db.flush()
            
            # 회사명 다국어 저장 (비어 있으면 빈 문자열로 대치)
            ko_name = row.get('company_ko', '').strip() 
            en_name = row.get('company_en', '').strip() 
            ja_name = row.get('company_ja', '').strip() 
            
            if ko_name:
                db.add(CompanyName(language='ko', name=ko_name, company_id=company.id))
            if en_name:
                db.add(CompanyName(language='en', name=en_name, company_id=company.id))
            if ja_name:
                db.add(CompanyName(language='ja', name=ja_name, company_id=company.id))
            
            # 태그 여러개 분리
            tag_ko_list = row.get('tag_ko','').split('|')
            tag_en_list = row.get('tag_en','').split('|')
            tag_ja_list = row.get('tag_ja','').split('|')
            
            
            for ko_tag, en_tag, ja_tag in zip(tag_ko_list, tag_en_list, tag_ja_list):
                ko_tag = ko_tag.strip()
                en_tag = en_tag.strip()
                ja_tag = ja_tag.strip()
                
                # 중복 검사
                tag = db.query(Tag).join(TagName).filter(TagName.language == 'ko', TagName.name == ko_tag).first()

                if not tag:
                    tag = Tag()
                    db.add(tag)
                    db.flush()
                    
                    # 태그명 다국어 저장
                    db.add(TagName(language='ko', name=ko_tag, tag_id=tag.id))
                    db.add(TagName(language='en', name=en_tag, tag_id=tag.id))
                    db.add(TagName(language='ja', name=ja_tag, tag_id=tag.id))
                db.add(CompanyTag(company_id=company.id, tag_id=tag.id))
                
        db.commit()
        db.close()
        print("Sample data loaded successfully.")
            
if __name__ == "__main__":
    load_csv_to_db("company_tag_sample.csv")