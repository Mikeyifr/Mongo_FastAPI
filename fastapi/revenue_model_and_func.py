from pydantic import BaseModel

class Revenue(BaseModel):
    company_name: str
    year: int
    revenue: str

# revenue class to dict for the get method
def revenue_dict(revenue) -> dict:
    return {
        "id": str(revenue["_id"]),
        "company_name": revenue["company_name"],
        "year": revenue["year"],
        "revenue": revenue["revenue"],
    }

# makes a list of dictionaries of revenues from a collection of Revenue class
def list_of_revenues(revenues):
    return [revenue_dict(revenue) for revenue in revenues]
