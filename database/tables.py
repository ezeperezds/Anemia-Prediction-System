from database.database import Base
from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime, timezone

class Prediction(Base):
    # Name of the table
    __tablename__ = 'predictions'
    
    # Columns of the table
    
    id = Column(Integer, 
                primary_key=True, 
                autoincrement=True)
    
    gender = Column(Integer, 
                    nullable=False)
    
    hemoglobin = Column(Float, 
                        nullable=False)
    
    mch = Column(Float, 
                nullable=False)
    
    mchc = Column(Float, 
                nullable=False)
    
    mcv = Column(Float, 
                nullable=False)
    
    prediction = Column(Integer,
                        nullable=False)
    
    diagnosis = Column(String,
                    nullable=False)
    
    probability = Column(Float,
                        nullable=False)
    
    created_at = Column(DateTime,
                        default= lambda: datetime.now(timezone.utc),
                        nullable=False)