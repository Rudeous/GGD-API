from http import client
from graphene.test import Client
from model import *
from schema import Query, Mutation, schema

"""
GIVEN a test database with 3 households
"""
def test_connection():
    conn = db_session.connection()
    assert conn is not None

def test_query_all_households():
    client = Client(schema)
    executed = client.execute('''
        query {
            allHouseholds {
                edges {
                    node {
                        householdId
                        housingType
                    }
                }
            }
        }
    ''')
    assert executed == {
        'data': {
            'allHouseholds': {
                'edges': [
                    {
                        'node': {
                            'householdId': '1',
                            'housingType': Housing_Type.landed.name
                        }
                    },
                    {
                        'node': {
                            'householdId': '2',
                            'housingType': Housing_Type.condo.name
                        }
                    },
                    {   
                        'node': {
                            'householdId': '3',
                            'housingType': Housing_Type.hdb.name
                        }
                    }
                ]
            }
        }
    }