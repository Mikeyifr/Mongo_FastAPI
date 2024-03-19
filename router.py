from pymongo import MongoClient
from fastapi import FastAPI
from pydantic import BaseModel
# pip install pymongo
# pip install fastapi
# pip install uvicorn
# pip install python-multipart


# MongoDB connection
username = "root"
password = "root"
client = MongoClient(f"mongodb://{username}:{password}@localhost:27017")
db = client.companies
collection = db.companies



# class company for the companies table
class Company(BaseModel):
    name: str
    field: str
    manager: str
    phone: str

# company class to dict for the get method
def company_dict(company) -> dict:
    return {
        "id": str(company["_id"]),
        "name": company["name"],
        "field": company["field"],
        "manager": company["manager"],
        "phone": company["phone"]
    }

# makes a list of dictionaries of comapnies from a collection of Company class
def list_of_companies(companies):
    return [company_dict(company) for company in companies]



app = FastAPI()

# company get method -> returns all of the companies
@app.get('/')
def get_companies():
    companies = list_of_companies(collection.find())
    return companies

# company post method -> adds a company of type Comapny
@app.post('/')
def post_company(company: Company):
    collection.insert_one(dict(company))

# company get method -> returns a specific company that matches the company name given
@app.get('/{name}')
def get_a_company(name: str):
    return company_dict(collection.find_one({"name": name}))
