import graphene
from graphene import relay, Field, String, List
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

    # return all entries
    all_households = SQLAlchemyConnectionField(Household.connection) 
    all_family_members = SQLAlchemyConnectionField(Family_Member.connection)

    # return individual entry
    household = Field(Household, h_id=graphene.String() ) # filter by household_id


    def resolve_household(cls, info, h_id): # filter households by household_id
        return db_session.query(HouseholdModel).filter_by(household_id=h_id).first()

    family_members = List(Family_Member, h_id=graphene.String()) # filter family_members by household_id
    def resolve_family_members(cls, info, h_id):
        return db_session.query(Family_MemberModel).filter_by(household_id=h_id).all() 
        # returns a list of family members in the household

"""
Mutations
"""

class CreateHousehold(graphene.Mutation):

    class Arguments:
        household_id = graphene.String()
        housing_type = Housing_Type(required=True)
    household = graphene.Field(lambda: Household)

    def mutate(self, info, household_id, housing_type):
        household = HouseholdModel(household_id = household_id, housing_type=housing_type)
        db_session.add(household)
        db_session.commit()
        return CreateHousehold(household=household)

class AddFamily_Member(graphene.Mutation):
    class Arguments:
        family_member_id = graphene.String(required=True)
        household_id = graphene.String(required=True)
        spouse_id = graphene.String(default_value=None, required=False)
        name = graphene.String(required=True)
        gender = Gender(required=True)
        marital_status = Marital_Status(required=True)
        occupation_type = Occupation_Type(required=True)
        annual_income = graphene.String(required=True)
        dob = graphene.Date(required=True)
    family_member = graphene.Field(lambda: Family_Member)

    def mutate(self, info, family_member_id, household_id, name, gender, marital_status, occupation_type, annual_income, dob, **kwargs):
        family_member = Family_MemberModel(family_member_id=family_member_id, household_id=household_id, name=name, gender=gender, \
            marital_status=marital_status, occupation_type=occupation_type, \
            annual_income=annual_income, dob=dob,)
        spouse_id = kwargs.get("spouse_id", None)
        Family_MemberModel.spouse_id = spouse_id # only married people have spouse_ids
        Family_MemberModel.occupation_type = Occupation_Type(occupation_type)
        db_session.add(family_member)
        db_session.commit()
        return AddFamily_Member(family_member=family_member)

class Mutation(graphene.ObjectType):
    create_household = CreateHousehold.Field()
    add_family_member = AddFamily_Member.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)