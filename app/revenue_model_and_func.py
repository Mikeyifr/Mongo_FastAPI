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
        if rev["revenue"][-1] == "k":
            this_year_revenue *= 1000
        if rev["revenue"][-1] == "m":
            this_year_revenue *= 1000000
        revenue_sum += this_year_revenue
    if revenue_sum < 1000000:
        revavg = str(round((revenue_sum / len(company_revenues) / 1000), 2)) + "k"
    else:
        revavg = str(round((revenue_sum / len(company_revenues) / 1000000), 2)) + "m"
    return revavg