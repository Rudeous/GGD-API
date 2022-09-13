from model import Gender, Housing_Type, Marital_Status, Occupation_Type
from datetime import date
import json

def generate_family_member_url(args): # input multidict args, output string
    res_str = "{"
    for key in args:
        res_str += f'{args[key]} '

    res_str = res_str.strip(' ') + "}"
    return res_str
    
def calculate_age(born): # input date object, output int
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def check_eligibility(household_list, grant): # student encouragement bonus
    """
    conditions:
    - Households with member(s) that is/are a student of less than 16 years old
    - Households income of less than $200,000. 
    qualifying members:
    - student of less than 16 years old
    input: list of household dicts
    output: json string with household and qualifying members
    """
    for household_dict in list(household_list):
        total_income = 0
        family_members_list = household_dict['node']['familyMembers']['edges']
        for family_member_dict in list(family_members_list):
            dob = family_member_dict['node']['dob']
            age = calculate_age(date.fromisoformat(dob))
            occupation_type = family_member_dict['node']['occupationType']
            housing_type = household_dict['node']['housingType']
            annual_income = family_member_dict['node']['annualIncome']
            total_income += int(annual_income)

            if grant == "SEB":
                if occupation_type != Occupation_Type.student.value or age >= 16:
                    # remove without returning
                    family_members_list.remove(family_member_dict)
                if total_income >= 200000:
                    # household income of more than $200,000 or no members eligible -> remove household
                    household_list.remove(household_dict)
                    break
            
            elif grant == "MS":
                # age < 18 or age > 55 -> whole household eligible
                # total_income < 150000 -> whole household eligible
                if total_income >= 150000:
                    household_list.remove(household_dict)
                    break
                if age < 18 or age > 55:
                    break
            
            elif grant == "EB":
                # household type != HDB or age < 55 -> remove family member
                if housing_type != Housing_Type.hdb.value or age < 55:
                    family_members_list.remove(family_member_dict)
            
            elif grant == "BSG":
                # age != 0 and older than 8 months -> remove family member
                age_month = (date.today().year - date.fromisoformat(dob).year) * 12 + date.today().month - date.fromisoformat(dob).month
                if age_month >= 8:
                    family_members_list.remove(family_member_dict)

            elif grant == "YGG":
                # total income > 100000 -> remove household
                # housing type != HDB -> remove household
                if total_income >= 100000 or housing_type != Housing_Type.hdb.value:
                    household_list.remove(household_dict)
                    break


    
    # clean empty household dicts
    for household_dict in list(household_list):
        if not household_dict['node']['familyMembers']['edges']:
            household_list.remove(household_dict)
    
    return json.dumps(household_list)

