import requests

def robyn_request():
  text = requests.get("http://localhost:8080").text
  if text != "":
    return text + " from Robyn"
  else:
    return "No response"


from starfyre import create_component

def fx_parent():
    component = create_component("""
    <div>{[ robyn_request() for i in range(2) ]}</div>

        """,
"""

""",
"""

"""
    )
    return component


parent=fx_parent()
    