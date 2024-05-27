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

def average_revenue(company_revenues):
    revenue_sum = 0
    for rev in company_revenues:
        this_year_revenue = int(rev["revenue"][0:-1])
        revenue_sum += this_year_revenue
    revavg = str(round(revenue_sum / len(company_revenues), 2)) + "k"
    return revavg