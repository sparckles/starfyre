from starfyre import create_component, render
import requests

def mock_request():
  return requests.get("http://localhost:8080").text + " from Robyn"


def fx_parent():
    component = create_component("""
    <div>{mock_request()}</div>

        """)

    return component


parent=fx_parent()
    