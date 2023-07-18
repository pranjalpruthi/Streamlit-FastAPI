from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta

app = FastAPI()

# Enable Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up SQLite DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./sample.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base: DeclarativeMeta = declarative_base()

class Sample(Base):
    __tablename__ = "samples"
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String)
    count = Column(Integer)

Base.metadata.create_all(bind=engine)



@app.get("/samples")
def get_samples():
    db = SessionLocal()
    samples = db.query(Sample.id, Sample.city, Sample.count).all()
    db.close()
    return [
        {"id": sample.id, "city": sample.city, "count": sample.count}
        for sample in samples
    ]


@app.post("/samples")
def add_sample(city: str, count: int):
    db = SessionLocal()
    sample = Sample(city=city, count=count)
    db.add(sample)
    db.commit()
    db.refresh(sample)
    db.close()
    return {"message": "Sample added successfully"}

@app.put("/samples/{sample_id}")
def update_sample(sample_id: int, city: str, count: int):
    db = SessionLocal()
    sample = db.query(Sample).filter(Sample.id == sample_id).first()
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")
    sample.city = city
    sample.count = count
    db.commit()
    db.close()
    return {"message": "Sample updated successfully"}

@app.delete("/samples/{sample_id}")
def delete_sample(sample_id: int):
    db = SessionLocal()
    sample = db.query(Sample).filter(Sample.id == sample_id).first()
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")
    db.delete(sample)
    db.commit()
    db.close()
    return {"message": "Sample deleted successfully"}


