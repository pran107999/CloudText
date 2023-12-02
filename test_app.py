import json
import pytest
import requests


BASE_URL = "https://ultra-thought-397322.uc.r.appspot.com/"



@pytest.fixture
def client():
    with requests.Session() as client:
        yield client

def test_index_route(client):
    response = client.get(BASE_URL)
    assert response.status_code == 200
    assert b'Text Summarization' in response.content



def test_show_summary_route_summary_not_found(client):
    response = client.get(BASE_URL + 'summary/100')
    
    assert response.status_code == 200
    assert b'Summary not found.' in response.content


