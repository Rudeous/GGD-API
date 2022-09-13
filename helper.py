from model import Gender, Marital_Status, Occupation_Type

def generate_family_member_url(args): # input multidict args, output string
    res_str = "{"
    for key in args:
        res_str += f'{args[key]} '

    res_str = res_str.strip(' ') + "}"
    return res_str
    