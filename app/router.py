from pymongo import MongoClient
from fastapi import FastAPI, HTTPException, status, Request, Form
from fastapi.responses import RedirectResponse
import company_model_and_func as comp
import revenue_model_and_func as rev
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
# pip install pymongo
# pip install fastapi
# pip install uvicorn
# pip install python-multipart


# MongoDB connection
username = "root"
password = "root"
client = MongoClient(f"mongodb://{username}:{password}@mongo")
db = client.companies
companies_collection = db.companies
revenues_collection = db.revenues

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/templates", StaticFiles(directory="templates"), name="templates")

def redirect_to_home(url: str = "/", status_code: int = 302):
     return RedirectResponse(url, status_code=status_code)


# companies get method -> returns all of the companies
@app.get('/')
def get_companies(request: Request):
    companies = comp.list_of_companies(companies_collection.find())
    if companies != []:
        headings = ["name","field","manager","phone"]
        return templates.TemplateResponse('list_of_companies.html', {'request': request, 'headings': headings, 'companies': companies})
    else:
        return "Sorry, There are no companies in the table"



# company and revenues get method -> returns the company info and revenues of the company name given
@app.get('/{company_name}')
def get_all_data_by_company_name(request: Request ,company_name: str):
    headings = ["year", "revenue"]
    company_info = get_a_company(company_name)
    company_revenues = get_revenues_for_company(company_name, is_func_req = 1)
    if company_revenues is None:
        company_revenues = []
        average_revenue = "No revenue record exist for this company"
    else:
        average_revenue = rev.average_revenue(company_revenues)
    return templates.TemplateResponse('info.html', {'request': request, 'headings': headings, 'company': company_info, 
                                                                 'revenues': company_revenues, 'avgrev': average_revenue })
# company get function -> returns a specific company that matches the company name given
def get_a_company(name: str):
    if companies_collection.find_one({"name": {"$eq" : name}}) != None:
        return comp.company_dict(companies_collection.find_one({"name": {"$eq" : name}}))
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
# revenues get function -> returns all of the revenues for a specific company
def get_revenues_for_company(company_name: str, is_func_req: int = 0):
# is_func_req is an indicator to whether the function is being called from the get_all_data_by_company_name and if so won't raise the 404
    revenues_of_a_company = rev.list_of_revenues(revenues_collection.find({"company_name": {"$eq": company_name}}).sort({"year" : -1}))
    if revenues_of_a_company != []:
        return revenues_of_a_company
    if is_func_req == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)



# companies get method -> returns all companies with the field that match the field given
@app.get('/field/{field}')
def get_companies_by_field(request: Request, field: str):
    company_by_field_list =  comp.list_of_companies(companies_collection.find({"field": {"$eq" : field}}))
    if company_by_field_list != []:
        headings = ["name","field","manager","phone"]
        return templates.TemplateResponse('sort_by_field.html', {'request': request, 'headings': headings, 'companies': company_by_field_list})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)



@app.get('/add/company')
def add_company_page(request: Request):
    return templates.TemplateResponse('add_a_company.html', {'request': request})
@app.post('/add/company')
def company_form(name: str = Form(...), field: str = Form(...), 
                 manager: str = Form(...), phone: str = Form(...)):
    company = comp.Company(name = name, field = field, manager = manager, phone = phone)
    post_company(company)
    return redirect_to_home()
def post_company(company: comp.Company):
    company = dict(company)
    if companies_collection.find_one({"name": {"$eq": company["name"]}}) == None:
        companies_collection.insert_one(company)
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)



# revenue post method -> adds a revenue of type Revenue
@app.get('/add/revenue')
def add_revenue_page(request: Request):
    return templates.TemplateResponse('add_a_revenue.html', {'request': request})
@app.post('/add/revenue')
def revenue_form(company_name: str = Form(...), year: int = Form(...), 
                 revenue: str = Form(...)):
    revenue = rev.Revenue(company_name = company_name, year = year, revenue = revenue)
    post_revenue(revenue)
    return redirect_to_home()
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
    


@app.get('/update/company/{update_company_name}')
def update_company_page(request: Request, update_company_name):
    return templates.TemplateResponse('update_company.html', {'request': request, 'update_company_name': update_company_name,
                                                               'company': get_a_company(update_company_name)})
@app.post('/update/company/{update_company_name}')
def update_company_form(update_company_name : str, name: str = Form(...), field: str = Form(...), 
                 manager: str = Form(...), phone: str = Form(...)):
    company = comp.Company(name = name, field = field, manager = manager, phone = phone)
    update_company(company, update_company_name)
    return redirect_to_home()
def update_company(updated_company: comp.Company, update_company_name: str):
    companies_collection.find_one_and_update({"name": update_company_name}, {"$set" : dict(updated_company)})



@app.get('/remove/company/{remove_company_name}')
def remove_company(remove_company_name : str):
    companies_collection.find_one_and_delete({"name": remove_company_name})
    revenues_collection.delete_many({"company_name":  remove_company_name})
    return redirect_to_home()
@app.get('/remove/revenue/{company_name}/{year}')
def remove_revenue(company_name : str, year : int):
    revenues_collection.find_one_and_delete({"company_name" : company_name, "year":  year})
    return redirect_to_home()