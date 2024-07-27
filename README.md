Updated README
text
# Rule Engine with AST

This project implements a simple 3-tier rule engine application using Flask, SQLAlchemy, and SQLite. It allows for the creation, combination, and evaluation of rules based on Abstract Syntax Trees (ASTs).

## Setup

1. Install the required dependencies:
   ```bash
   pip install flask sqlalchemy

Run the Flask application:
bash
python main.py

**COMPONENTS**

1. Backend :  main.py (Flask Python SQLAlchemy)
2. Frontend : rlg.py (Tkinter UI Python)
3. Automated test script : test.py (Automatically test the app) (requests)


**APP COMPONENTS**

1. CREATE RULE : will create a rule and show id in UI. for eg: you create two rules it will create two rules with id 1 and 2
2. Combine RULE: for eg : you add rule number id with comma separated format, it will create a mega rule with separate id on the tkinteR UI
3. EVALUATE RULE : Add the mega rule Id and data params that you need to provide in json format


**API Endpoints**

1. Create Rule
URL: /create_rule
Method: POST
Data Params:
json
{
  "rule_string": "(age > 30 AND department = 'Sales') OR (salary > 50000)"
}

Success Response:
json
{
  "id": 1,
  "ast": "..."
}

2. Combine Rules
URL: /combine_rules
Method: POST
Data Params:
json
{
  "rule_ids": [1, 2]
}

Success Response:
json
{
  "id": 3,
  "combined_ast": "..."
}

3. Evaluate Rule
URL: /evaluate_rule
Method: POST
Data Params:
json
{
  "rule_id": 3,
  "data": {
    "age": 35,
    "department": "Sales",
    "salary": 60000,
    "experience": 6
  }
}

Success Response:
json
{
  "result": true
}

4. Modify Rule
URL: /modify_rule
Method: POST
Data Params:
json
{
  "rule_id": 1,
  "new_rule_string": "age > 40 AND department = 'HR'"
}

Success Response:
json
{
  "message": "Rule updated successfully"
}

Sample Curl Workflow
Here's a step-by-step workflow using curl commands to test the rule engine:
Create the first rule:
bash
curl -X POST http://127.0.0.1:5000/create_rule -H "Content-Type: application/json" -d '{"rule_string": "(age > 30 AND department = '\''Sales'\'') OR (salary > 50000)"}'

Create the second rule:
bash
curl -X POST http://127.0.0.1:5000/create_rule -H "Content-Type: application/json" -d '{"rule_string": "experience > 5 AND department = '\''Marketing'\''"}'

Combine the rules (replace 1 and 2 with the actual rule IDs from steps 1 and 2):
bash
curl -X POST http://127.0.0.1:5000/combine_rules -H "Content-Type: application/json" -d '{"rule_ids": [1, 2]}'

Evaluate the combined rule (replace 3 with the actual combined rule ID from step 3):
bash
curl -X POST http://127.0.0.1:5000/evaluate_rule -H "Content-Type: application/json" -d '{
  "rule_id": 3,
  "data": {
    "age": 35,
    "department": "Sales",
    "salary": 60000,
    "experience": 6
  }
}'

Modify a rule (replace 1 with the actual rule ID you want to modify):
bash
curl -X POST http://127.0.0.1:5000/modify_rule -H "Content-Type: application/json" -d '{
  "rule_id": 1,
  "new_rule_string": "age > 40 AND department = '\''HR'\''"
}'

Testing
You can use the provided test.py script to test the rule engine functionality. Run it using:
bash
python test.py

This script will test creating rules, combining rules, evaluating rules, and modifying rules.
test.py Script
Here is the test.py script for automated testing:
python
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_create_rule(rule_string):
    print("Testing create_rule...")
    url = f"{BASE_URL}/create_rule"
    data = {"rule_string": rule_string}
    response = requests.post(url, json=data)
    print(f"Response: {response.json()}")
    return response.json()['id']

def test_combine_rules(rule_id_1, rule_id_2):
    print("\nTesting combine_rules...")
    url = f"{BASE_URL}/combine_rules"
    data = {"rule_ids": [rule_id_1, rule_id_2]}
    response = requests.post(url, json=data)
    print(f"Response: {response.json()}")
    return response.json()['id']

def test_evaluate_rule(rule_id, data):
    print("\nTesting evaluate_rule...")
    url = f"{BASE_URL}/evaluate_rule"
    data = {"rule_id": rule_id, "data": data}
    response = requests.post(url, json=data)
    print(f"Response: {response.json()}")

def test_modify_rule(rule_id, new_rule_string):
    print("\nTesting modify_rule...")
    url = f"{BASE_URL}/modify_rule"
    data = {"rule_id": rule_id, "new_rule_string": new_rule_string}
    response = requests.post(url, json=data)
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    # Create Rule 1
    rule_string_1 = "(age > 30 AND department = 'Sales')"
    rule_id_1 = test_create_rule(rule_string_1)

    # Create Rule 2
    rule_string_2 = "(salary > 50000 OR experience > 5)"
    rule_id_2 = test_create_rule(rule_string_2)

    # Combine Rules
    combined_rule_id = test_combine_rules(rule_id_1, rule_id_2)

    # Evaluate Combined Rule
    data = {
        "age": 35,
        "department": "Sales",
        "salary": 60000,
        "experience": 6
    }
    test_evaluate_rule(combined_rule_id, data)

    # Modify Rule
    new_rule_string = "age > 40 AND department = 'HR'"
    test_modify_rule(rule_id_1, new_rule_string)

Summary
This updated README provides clear instructions on setting up, running, and testing the rule engine application. The test.py script automates the testing process, ensuring that the rule engine's functionality is verified correctly. By following these instructions, you can ensure that your rule engine application is working as expected.
