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
