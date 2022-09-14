# GGD-API
## Government Grant Disbursement (GGD) API
A RESTful API to help decide on groups of people who are eligible for various upcoming government grants. 
These grants are disbursed based on certain criteria - like total household income, age, occupation, etc. The API can build up a list of recipients and which households qualify for it. 
For ease of definition, a household is defined by all the people living inside 1 physical housing unit.

## Setup
### Local
#### Setting up a virtual environment
If you have not set up your virtual environment, it is recommended that you do so and activate it to install the modules used in this project.

Windows
```
python -m venv venv
venv\Scripts\activate

```
This prevents any conflicts between the Python packages used in this project and the packages in your local machine.

#### Install packages
Install the required python packages on your virtual environment
```
pip install -r requirements.txt
```

#### Running the Flask apps
Run flask apps (endpoint controller or graphql) with
```
python controller.py
python gql_app.py
```

### Docker
#### Docker Check
Ensure that Docker is installed and running on you machine

#### Build Docker images
In the root of the project folder where the `docker-compose.yml` file is, run 
```
docker-compose build
```

#### Start Containers
After the images have been built, run
```
docker-compose up
```

## Testing
Use the provided postman collection to test endpoints at https://www.getpostman.com/collections/b4370d551777da8246b7

## Assumptions
### Endpoints
1. **Create Households**
    

2. **Add a family member to household**
    - All listed fields except spouse (should the marital status be "single") are required

3. **List all households**
    - household details are retrieved, along with family member details

4. **Search for a specific household**
    - search is by household identifier (householdId) in order to get single, specific household

5. **List the households and qualifying family members of grant disbursement**
    - Only one type of grand is checked for at one time


### Miscellaneous
- **Monogamous relationships** - each family member can have at most 1 spouse 
- **Marital status** - the GGD is only concerned with the marital statuses of "Single" and "Married"