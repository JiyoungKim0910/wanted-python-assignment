from typing import Dict, List
from pydantic import BaseModel, Field

class TagNameSchema(BaseModel):
    tag_name: Dict[str, str] = Field(
        ..., description="다국어 태그명"
        , example={"en": "tag1", "ko":"태그1"}
    )

class CompanyResponseSchema(BaseModel):
    company_name : str = Field(..., description="요청 언어 기준의 회사명")
    tags: List[str] = Field(..., description="요청 언어 기준의 태그 목록")
    
class TagUpdateSchema(BaseModel):
    tag_name: Dict[str, str] = Field(..., description="추가 또는 삭제할 태그명(언어코드 포함)")
    
class CompanyCreateSchema(BaseModel):
    company_name: Dict[str, str] = Field(
        ..., description="다국어 회사명"
            ,example={"en": "Wantedlab", "ko": "원티드랩"} 
    )
    tags: List[TagNameSchema]