import os
from flask import Flask, render_template, request, jsonify, json
from flask_graphql import GraphQLView
from model import Household, Housing_Type, Gender, Marital_Status, Occupation_Type
import requests
from enum import Enum
from helper import *
from flask_cors import CORS

app = Flask(__name__)

# graphql_URL = "http://127.0.0.1:5001/graphql" # local
graphql_URL = "http://gql_app:5001/graphql" # docker
CORS(app)

@app.route('/hello')
def hello():
    return "Hello World!"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_household', methods=['POST'])
def create_household():
    data = request.args
    print(data)

    housing_type = Housing_Type[data['housing_type']].name
    gql_households_response = requests.get(graphql_URL+'?query=query{allHouseholds{edges{node{householdId housingType}}}}')
    gql_households_json = gql_households_response.json()
    print(gql_households_json)
    household_sort_list = []
    for household in gql_households_json['data']['allHouseholds']['edges']:
        household["node"]["householdId"] = int(household["node"]["householdId"]) # convert householdId to int
        household_sort_list.append(household["node"]) # append household to list

    # sort list of household objects by householdId
    household_sort_list.sort(key=lambda x: x["householdId"]) 

    # after ordering by householdId in asc order, retrieve the last householdId
    largest_householdId = household_sort_list[-1]["householdId"]

    # increment the largest householdId by 1 to get the new householdId to be created
    new_householdId = str(largest_householdId + 1)

    household_post_url = graphql_URL +  '?query=mutation{createHousehold' + \
        f'(householdId:"{new_householdId}",housingType:{housing_type})' + \
        '{household{householdId housingType}}}'
    household_post_response = requests.post(household_post_url)
    return json.dumps(household_post_response.json(), indent=4), household_post_response.status_code

@app.route('/add_family_member', methods=['POST'])
def add_family_member():
    data = request.args

    # retrieve required fields to create a new family member entry
    household_id = data['household_id']
    name = data['name']
    gender = Gender[data['gender']].name
    marital_status = Marital_Status[data['marital_status']].name
    spouse_id = data.get('spouse_id', None)
    occupation_type = Occupation_Type[data['occupation_type']].name
    annual_income = data['annual_income']
    dob = data['dob']

    gql_family_members_response = requests.get(graphql_URL+'?query=query{allFamilyMembers{edges{node{familyMemberId}}}}')
    gql_family_members_json = gql_family_members_response.json()
    family_member_sort_list = []
    for family_member in gql_family_members_json['data']['allFamilyMembers']['edges']:
        family_member["node"]["familyMemberId"] = int(family_member["node"]["familyMemberId"])
        family_member_sort_list.append(family_member["node"])
    
    family_member_sort_list.sort(key=lambda x: x["familyMemberId"])
    largest_familyMemberId = family_member_sort_list[-1]["familyMemberId"]
    new_familyMemberId = str(largest_familyMemberId + 1)


    add_family_member_url = graphql_URL + '?query=mutation{addFamilyMember' + \
        f'(familyMemberId:"{new_familyMemberId}" ,householdId:"{household_id}",name:"{name}", gender:{gender}, maritalStatus:{marital_status}, \
            spouseId:"{spouse_id}", occupationType:{occupation_type}, annualIncome:"{annual_income}", dob:"{dob}")' + \
        '{familyMember{familyMemberId householdId name gender maritalStatus spouseId occupationType annualIncome dob}}}'
    add_family_member_response = requests.post(add_family_member_url)
    return json.dumps(add_family_member_response.json(), indent=4), add_family_member_response.status_code


@app.route('/list_all_households', methods=['GET'])
def list_all_households():
    # retrieve arguments to retrieve from request
    args = request.args

    # build url to query graphql server for households with family fields specified
    gql_households_response = requests.get(graphql_URL\
        +'?query=query{allHouseholds{edges{node{householdId housingType familyMembers{edges{node' \
        + generate_family_member_url(args) + '}}}}}}')
    gql_households_json = gql_households_response.json()
    return json.dumps(gql_households_json, indent=4), gql_households_response.status_code

@app.route('/search_specific_household', methods=['GET'])
def search_specific_household():
    args = request.args # search by householdId since to get a specific household
    # convert args to mutable dict
    args = dict(args)
    household_id = args['household_id']
    args.pop('household_id') # remove household_id from args since it is not a family member field

    url = graphql_URL+'?query={household(hId:"'+household_id\
        +'"){housingType familyMembers{edges{node' \
        + generate_family_member_url(args) + '}}}}'
    print(url)
    gql_household_response = requests.get(graphql_URL+'?query={household(hId: '+household_id\
        +'){housingType familyMembers{edges{node' \
        + generate_family_member_url(args) + '}}}}')
    gql_household_json = gql_household_response.json()
    return json.dumps(gql_household_json, indent=4), gql_household_response.status_code

@app.route('/list_eligible', methods=['GET'])
def list_eligible():
    args = request.args # selection of grants to list eligible households and family members for
    grant = args['grant']
    # build url to query graphql server for all households with family fields specified
    gql_households_response = requests.get(graphql_URL\
        +'?query=query{allHouseholds{edges{node{householdId housingType familyMembers{edges{node' +\
            '{familyMemberId spouseId name gender maritalStatus occupationType annualIncome dob} }}}}}}')
    gql_households_json = gql_households_response.json()
    # print(gql_households_json)
    
    household_list = gql_households_json['data']['allHouseholds']['edges'] # list of household_dict


    # process json by passing into function to filter out ineligible households and family members
    seb_eligible = check_eligibility(household_list, grant)
    
    return seb_eligible

if __name__ == "__main__":
    # run seed data script to populate database with seed data
    os.system('python seed_db.py')
    app.run(port=5002, debug=True, host='0.0.0.0')

