from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)
    resumes = relationship("Resume", back_populates="user")

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String(255))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship("User", back_populates="resumes")

class JobMatch(Base):
    __tablename__ = "job_matches"
    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    job_url = Column(String(500))
    job_title = Column(String(255))
    ats_score = Column(Integer)
    tailored_resume = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class PromptVersion(Base):
    __tablename__ = "prompts"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    version = Column(String(20))
    template = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class UsageLog(Base):
    __tablename__ = "usage_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tokens_used = Column(Integer)
    cost = Column(String(50))
    provider = Column(String(50))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
