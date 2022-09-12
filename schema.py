from email.policy import default
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from model import Household as HouseholdModel, Family_Member as Family_MemberModel, db_session, \
    Housing_Type as Housing_Type_Enum , Gender as Gender_Enum , \
    Marital_Status as Marital_Status_Enum, Occupation_Type as Occupation_Type_Enum
from graphene_sqlalchemy.types import ORMField

# use predefined python enum in graphene
Housing_Type = graphene.Enum.from_enum(Housing_Type_Enum)
Gender = graphene.Enum.from_enum(Gender_Enum)
Marital_Status = graphene.Enum.from_enum(Marital_Status_Enum)
Occupation_Type = graphene.Enum.from_enum(Occupation_Type_Enum)

"""
purpose: to convert the SQLAlchemy models to Graphene objects with a graph schema
"""
class Household(SQLAlchemyObjectType):
    class Meta:
        model = HouseholdModel
        interfaces = (relay.Node, )
    housing_type = ORMField(type=Housing_Type) # use sqlalchemy enum instead of graphene enum

class Family_Member(SQLAlchemyObjectType):
    class Meta:
        model = Family_MemberModel
        interfaces = (relay.Node, )
    gender = ORMField(type=Gender)
    marital_status = ORMField(type=Marital_Status)
    occupation_type = ORMField(type=Occupation_Type)

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_households = SQLAlchemyConnectionField(Household.connection) 
    all_family_members = SQLAlchemyConnectionField(Family_Member.connection)



"""
Mutations
"""

class CreateHousehold(graphene.Mutation):

    class Arguments:
        household_id = graphene.Int()
        housing_type = Housing_Type(required=True)
    household = graphene.Field(lambda: Household)

    def mutate(self, info, household_id, housing_type):
        household = HouseholdModel(household_id = household_id, housing_type=housing_type)
        db_session.add(household)
        db_session.commit()
        return CreateHousehold(household=household)

class CreateFamily_Member(graphene.Mutation):
    class Arguments:
        family_member_id = graphene.Int(required=True)
        household_id = graphene.Int(required=True)
        spouse_id = graphene.Int(default_value=None, required=False)
        name = graphene.String(required=True)
        gender = Gender(required=True)
        marital_status = Marital_Status(required=True)
        occupation_type = Occupation_Type(required=True)
        annual_income = graphene.Int(required=True)
        dob = graphene.Date(required=True)
    family_member = graphene.Field(lambda: Family_Member)

    def mutate(self, info, family_member_id, household_id, name, gender, marital_status, occupation_type, annual_income, dob, **kwargs):
        family_member = Family_MemberModel(family_member_id=family_member_id, household_id=household_id, name=name, gender=gender, \
            marital_status=marital_status, occupation_type=occupation_type, \
            annual_income=annual_income, dob=dob,)
        spouse_id = kwargs.get('spouse_id', None)
        Family_MemberModel.spouse_id = spouse_id # only married people have spouse_ids
        Family_MemberModel.occupation_type = Occupation_Type(occupation_type)
        db_session.add(family_member)
        db_session.commit()
        return CreateFamily_Member(family_member=family_member)

class Mutation(graphene.ObjectType):
    create_household = CreateHousehold.Field()
    create_family_member = CreateFamily_Member.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)