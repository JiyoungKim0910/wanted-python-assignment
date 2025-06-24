from functools import wraps
from fastapi import HTTPException
from sqlalchemy.orm import Session

def transactional(func):
    
    @wraps(func)
    def wrapper(*args,**kwargs):
        db: Session = kwargs.get("db")
        if db is None:
            raise ValueError("A Session must be passed as a keyword arguments")
        try:
            result = func(*args,  **kwargs)
            db.commit()
            return result
        except HTTPException:
            db.rollback()
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
    
    return wrapper