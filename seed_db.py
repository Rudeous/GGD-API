from model import *
from schema import Query, Mutation, schema
import os
from datetime import datetime, date


# delete db if exists
if os.path.exists('database.sqlite3'):
    db_session.close()
    Base.metadata.drop_all(bind=engine) 
    os.remove('database.sqlite3')

# start db session
conn = db_session.connection()

# create tables in db if not done
Base.metadata.create_all(bind=engine)

# household population
household1 = Household(household_id='1', housing_type=Housing_Type.landed)
household2 = Household(household_id='2', housing_type=Housing_Type.condo)
household3 = Household(household_id='3', housing_type=Housing_Type.hdb)

# family member population
family_member1 = Family_Member(
    family_member_id='1', 
    household_id='1', 
    name='John', 
    gender=Gender.male, 
    marital_status=Marital_Status.married, 
    spouse_id='2', 
    occupation_type=Occupation_Type.employed, 
    annual_income='3000', 
    dob= datetime.strptime('1980-01-01', "%Y-%m-%d")
    )

family_member2 = Family_Member(
    family_member_id='2', 
    household_id='1', 
    name='Mary', 
    gender=Gender.female, 
    marital_status=Marital_Status.married, 
    spouse_id='1', 
    occupation_type=Occupation_Type.employed,
    annual_income='3100',
    dob= datetime.strptime('1985-02-02', "%Y-%m-%d")
    )

# add to db
db_session.add(household1)
db_session.add(household2)
db_session.add(household3)

db_session.add(family_member1)
db_session.add(family_member2)

# commit to db
db_session.commit()