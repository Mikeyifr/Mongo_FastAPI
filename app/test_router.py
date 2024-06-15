from fastapi.testclient import TestClient
from router import app
testclient = TestClient(app)



def test_list_of_companies():
    respose = testclient.get("/")
    assert respose.status_code == 200

def test_add_company_page():
    respose = testclient.get("/add/company")
    assert respose.status_code == 200

def test_add_company():
    form_data = {"name": "testcompany", "field": "testfield", "manager": "test manager", "phone": "test number"}
    respose = testclient.post("/add/company", data=form_data)
    assert respose.status_code == 200

def test_add_revenue_page():
    respose = testclient.get("/add/revenue")
    assert respose.status_code == 200

def test_add_revenue():
    form_data = {"company_name": "testcompany","year": 2023, "revenue": "200k"}
    respose = testclient.post("/add/revenue", data=form_data)
    assert respose.status_code == 200

def test_info():
    respose = testclient.get("/testcompany")
    assert respose.status_code == 200

def test_sort_by_field():
    respose = testclient.get("/field/testfield")
    assert respose.status_code == 200

def test_update_company_page():
    respose = testclient.get("/update/company/testcompany")
    assert respose.status_code == 200

def test_update_company():
    form_data = {"name": "testcompany", "field": "testfield", "manager": "test manager", "phone": "updated test number"}
    respose = testclient.post("/update/company/testcompany", data=form_data)
    assert respose.status_code == 200

def test_remove_revenue():
    respose = testclient.get("/remove/revenue/testcompany/2023")
    assert respose.status_code == 200


def test_remove_company():
    respose = testclient.get("/remove/company/testcompany")
    assert respose.status_code == 200