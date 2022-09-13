from datetime import date
from mimetypes import init
import os
from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship, backref)
from sqlalchemy.ext.declarative import declarative_base
import sqlite3
from sqlite3 import Error
import enum
from flask import Flask, request, jsonify, render_template, redirect, url_for, json
from flask_cors import CORS
from flask_graphql import GraphQLView
from flask_sqlalchemy import SQLAlchemy

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
# from model import Household as HouseholdModel, Family_Member as Family_MemberModel


engine = create_engine('sqlite:///database.sqlite3') 
db_session = scoped_session(sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind=engine))

Base = declarative_base() # table creation
Base.query = db_session.query_property() # query execution

class Housing_Type(enum.Enum):
    landed = "landed"
    condo = "condo"
    hdb = "hdb"

class Gender(enum.Enum):
    male = "male"
    female = "female"

class Marital_Status(enum.Enum):
    married = "married"
    single = "single"

class Occupation_Type(enum.Enum):
    employed = "employed"
    unemployed = "unemployed"
    student = "student"

class Household(Base):
    __tablename__ = 'household'
    household_id = Column(String(256), primary_key=True)
    housing_type = Column(Enum(Housing_Type))

class Family_Member(Base):
    __tablename__ = 'family_member'
    family_member_id = Column(String(256), primary_key=True)
    household_id = Column(String(256), ForeignKey('household.household_id'))
    name = Column(String(256))
    gender = Column(Enum(Gender)) 
    marital_status = Column(Enum(Marital_Status))
    spouse_id = Column(String(256), ForeignKey('family_member.family_member_id'))
    occupation_type = Column(Enum(Occupation_Type))
    annual_income = Column(String(256))
    dob = Column(Date)
    household = relationship(
        "Household",
        primaryjoin=(household_id == Household.household_id),
        uselist= False, backref='family_members', 
        )



