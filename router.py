from pymongo import MongoClient
from fastapi import FastAPI, HTTPException, status
import company_model_and_func as comp
import revenue_model_and_func as rev
# pip install pymongo
# pip install fastapi
# pip install uvicorn
# pip install python-multipart



# MongoDB connection
username = "root"
password = "root"
client = MongoClient(f"mongodb://{username}:{password}@localhost:27017")
db = client.companies
companies_collection = db.companies
revenues_collection = db.revenues



app = FastAPI()
# companies get method -> returns all of the companies
@app.get('/')
def get_companies():
    companies = comp.list_of_companies(companies_collection.find())
    if companies != []:
        return companies
    else:
        return "Sorry, There are no companies in the table"

# company post method -> adds a company of type Comapny
@app.post('/')
def post_company(company: comp.Company):
    company = dict(company)
    if companies_collection.find_one({"name": {"$eq": company["name"]}}) == None:
        companies_collection.insert_one(company)
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

# company get method -> returns a specific company that matches the company name given
@app.get('/{name}')
def get_a_company(name: str):
    if companies_collection.find_one({"name": {"$eq" : name}}) != None:
        return comp.company_dict(companies_collection.find_one({"name": {"$eq" : name}}))
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

# companies get method -> returns all companies with the field that match the field given
@app.get('/field/{field}')
def get_companies_by_field(field: str):
    company_by_field_list =  comp.list_of_companies(companies_collection.find({"field": {"$eq" : field}}))
    if company_by_field_list != []:
        return company_by_field_list
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

# revenues get method -> returns all of the revenues for a specific company
@app.get('/revenues/{company_name}')
def get_revenues_for_company(company_name: str, is_func_req: int = 0):
# is_func_req is an indicator to whether the function is being called from the get_all_data_by_company_name and if so won't raise the 404
    revenues_of_a_company = rev.list_of_revenues(revenues_collection.find({"company_name": {"$eq": company_name}}))
    if revenues_of_a_company != []:
        return revenues_of_a_company
    if is_func_req == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return "No revenue records exist for this company"
    

# revenue post method -> adds a revenue of type Revenue
@app.post('/revenues')
def post_revenue(revenue: rev.Revenue):
    revenue = dict(revenue)
    for company in comp.list_of_companies(companies_collection.find()):
        if company["name"] == revenue["company_name"]:
            if revenues_collection.find_one({"company_name": {"$eq": revenue["company_name"]}, "year": {"$eq": revenue["year"]}}) == None:
                revenues_collection.insert_one(revenue)
                return None
            else:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        
# company and revenues get method -> returns the company info and revenues of the company name given
@app.get('/all/{company_name}')
def get_all_data_by_company_name(company_name: str):
    all_data = []
    all_data.append(get_a_company(company_name))
    all_data.append(get_revenues_for_company(company_name, is_func_req = 1))
    return all_data
