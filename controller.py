from flask import Flask, render_template, request, jsonify, json
from flask_graphql import GraphQLView
from model import Housing_Type, Gender, Marital_Status, Occupation_Type
import requests
from enum import Enum

app = Flask(__name__)

graphql_URL = "http://127.0.0.1:5001/graphql"

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
    print(household_post_response.json())
    print(household_post_response.status_code)
    return json.dumps(household_post_response.json(), indent=4), household_post_response.status_code

@app.route('/add_family_member', methods=['POST'])
def add_family_member():
    data = request.args
    print(data)

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
    print(gql_family_members_json)
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
    print(add_family_member_response.json())
    print(add_family_member_response.status_code)
    return json.dumps(add_family_member_response.json(), indent=4), add_family_member_response.status_code

if __name__ == "__main__":
    app.run(port=5002, debug=True)

