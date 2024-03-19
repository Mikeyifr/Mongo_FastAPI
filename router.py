from pymongo import MongoClient
from fastapi import FastAPI
import company_model_and_func as comp
import revenue_model_and_func as rev
from http import HTTPStatus
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
    return companies

# company post method -> adds a company of type Comapny
@app.post('/')
def post_company(company: comp.Company):
    companies_collection.insert_one(dict(company))

# company get method -> returns a specific company that matches the company name given
@app.get('/{name}')
def get_a_company(name: str):
    return comp.company_dict(companies_collection.find_one({"name": name}))

# companies get method -> returns all companies with the field that match the field given
@app.get('/field/{field}')
def get_companies_by_field(field: str):
    company_by_field_list =  comp.list_of_companies(companies_collection.find({"field": {"$eq" : field}}))
    return company_by_field_list

# revenues get method -> returns all of the revenues for a specific company
@app.get('/revenues/{company_name}')
def get_revenues_for_company(company_name: str):
    revenues_of_a_company = rev.list_of_revenues(revenues_collection.find({"company_name": {"$eq": company_name}}))
    return revenues_of_a_company

# revenue post method -> adds a revenue of type Revenue
@app.post('/revenues')
def post_revenue(revenue: rev.Revenue):
    revenue = dict(revenue)
    for company in comp.list_of_companies(companies_collection.find()):
        if company["name"] == revenue["company_name"]:
            revenues_collection.insert_one(revenue)
            return HTTPStatus.OK
    return HTTPStatus.NOT_FOUND
        
# company and revenues get method -> returns the company info and revenues of the company name given 
@app.get('/all/{company_name}')
def get_all_data_by_company_name(company_name: str):
    all_data = []
    all_data.append(comp.company_dict(companies_collection.find_one({"name": company_name})))
    all_data.append(rev.list_of_revenues(revenues_collection.find({"company_name": {"$eq": company_name}})))
    return all_data