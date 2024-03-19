from pydantic import BaseModel

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