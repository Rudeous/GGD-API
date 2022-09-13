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
household4 = Household(household_id='4', housing_type=Housing_Type.hdb)
household5 = Household(household_id='5', housing_type=Housing_Type.condo)
household6 = Household(household_id='6', housing_type=Housing_Type.landed)

# family member population
family_member1 = Family_Member(
    family_member_id='1', 
    household_id='1', 
    name='John', 
    gender=Gender.male, 
    marital_status=Marital_Status.single, 
    occupation_type=Occupation_Type.student, 
    annual_income='3000', 
    dob= datetime.strptime('2011-01-01', "%Y-%m-%d")
    )

family_member2 = Family_Member(
    family_member_id='2', 
    household_id='1', 
    name='Mary', 
    gender=Gender.female, 
    marital_status=Marital_Status.single, 
    occupation_type=Occupation_Type.student,
    annual_income='3100',
    dob= datetime.strptime('2012-02-02', "%Y-%m-%d")
    )

family_member3 = Family_Member(
    family_member_id='3', 
    household_id='2', 
    name='Ben', 
    gender=Gender.male, 
    marital_status=Marital_Status.single, 
    occupation_type=Occupation_Type.student,
    annual_income='0',
    dob= datetime.strptime('2013-03-03', "%Y-%m-%d")
    )

family_member4 = Family_Member(
    family_member_id='4', 
    household_id='2', 
    name='Sue', 
    gender=Gender.female, 
    marital_status=Marital_Status.single, 
    occupation_type=Occupation_Type.employed,
    annual_income='50000',
    dob= datetime.strptime('1950-04-04', "%Y-%m-%d")
    )

family_member5 = Family_Member(
    family_member_id='5', 
    household_id='3', 
    name='Tom', 
    gender=Gender.male, 
    marital_status=Marital_Status.married, 
    spouse_id='6', 
    occupation_type=Occupation_Type.employed,
    annual_income='1500000',
    dob= datetime.strptime('1940-05-05', "%Y-%m-%d")
    )

family_member6 = Family_Member(
    family_member_id='6', 
    household_id='3', 
    name='Sherry', 
    gender=Gender.female, 
    marital_status=Marital_Status.married, 
    spouse_id='5', 
    occupation_type=Occupation_Type.employed,
    annual_income='10000',
    dob= datetime.strptime('1940-06-06', "%Y-%m-%d")
    )

family_member7 = Family_Member(
    family_member_id='7', 
    household_id='4', 
    name='Harry', 
    gender=Gender.male, 
    marital_status=Marital_Status.single, 
    occupation_type=Occupation_Type.unemployed,
    annual_income='0',
    dob= datetime.strptime('2022-07-07', "%Y-%m-%d")
    )

family_member8 = Family_Member(
    family_member_id='8', 
    household_id='4', 
    name='Salynn', 
    gender=Gender.female, 
    marital_status=Marital_Status.single,  
    occupation_type=Occupation_Type.employed,
    annual_income='40000',
    dob= datetime.strptime('1980-08-08', "%Y-%m-%d")
    )

# add to db
db_session.add(household1)
db_session.add(household2)
db_session.add(household3)
db_session.add(household4)
db_session.add(household5)
db_session.add(household6)

db_session.add(family_member1)
db_session.add(family_member2)
db_session.add(family_member3)
db_session.add(family_member4)
db_session.add(family_member5)
db_session.add(family_member6)
db_session.add(family_member7)
db_session.add(family_member8)


# commit to db
db_session.commit()