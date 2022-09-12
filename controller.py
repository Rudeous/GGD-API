import imp
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


if __name__ == "__main__":
    app.run(port=5002, debug=True)

