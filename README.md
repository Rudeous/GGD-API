# GGD-API
## Government Grant Disbursement (GGD) API
A RESTful API to help decide on groups of people who are eligible for various upcoming government grants. 
These grants are disbursed based on certain criteria - like total household income, age, occupation, etc. The API can build up a list of recipients and which households qualify for it. 
For ease of definition, a household is defined by all the people living inside 1 physical housing unit.

## Setup

## Assumptions
- **Monogamous relationships** - each family member can have at most 1 spouse 
- **Marital status** - the GGD is only concerned with the marital statuses of "Single" and "Married"
