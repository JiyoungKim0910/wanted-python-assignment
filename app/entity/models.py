from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    company_name = relationship("CompanyName", back_populates="company",cascade="all,delete")
    tags = relationship("CompanyTag", back_populates="company", cascade="all,delete", lazy="joined")
    
class CompanyName(Base):
    __tablename__ = "company_names"
    id = Column(Integer, primary_key=True)
    language = Column(String, nullable=False) # 언어코드
    name = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="company_name")
    
class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    tag_names = relationship("TagName",back_populates="tag",cascade="all,delete")
    company_tags = relationship("CompanyTag",back_populates="tag",cascade="all, delete")
    
class TagName(Base):
    __tablename__ = "tag_names"
    id = Column(Integer, primary_key=True)
    language = Column(String, nullable=False) # 언어 코드
    name = Column(String, nullable=False)
    tag_id = Column(Integer,ForeignKey("tags.id"))
    tag = relationship("Tag", back_populates="tag_names")
    
class CompanyTag(Base):
    __tablename__ = "company_tags"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    tag_id = Column(Integer, ForeignKey("tags.id"))
    company = relationship("Company",back_populates="tags")
    tag = relationship("Tag",back_populates="company_tags")