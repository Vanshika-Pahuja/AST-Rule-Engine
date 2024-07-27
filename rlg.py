
import tkinter as tk
from tkinter import messagebox
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

class RuleEngineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rule Engine GUI")

        # Create Rule
        self.create_rule_frame = tk.Frame(root)
        self.create_rule_frame.pack(pady=10)
        tk.Label(self.create_rule_frame, text="Create Rule").pack()
        self.rule_string_entry = tk.Entry(self.create_rule_frame, width=50)
        self.rule_string_entry.pack()
        self.create_rule_button = tk.Button(self.create_rule_frame, text="Create Rule", command=self.create_rule)
        self.create_rule_button.pack()

        # Combine Rules
        self.combine_rule_frame = tk.Frame(root)
        self.combine_rule_frame.pack(pady=10)
        tk.Label(self.combine_rule_frame, text="Combine Rules (comma-separated IDs)").pack()
        self.rule_ids_entry = tk.Entry(self.combine_rule_frame, width=50)
        self.rule_ids_entry.pack()
        self.combine_rule_button = tk.Button(self.combine_rule_frame, text="Combine Rules", command=self.combine_rules)
        self.combine_rule_button.pack()

        # Evaluate Rule
        self.evaluate_rule_frame = tk.Frame(root)
        self.evaluate_rule_frame.pack(pady=10)
        tk.Label(self.evaluate_rule_frame, text="Evaluate Rule (Mega Rule ID)").pack()
        self.mega_rule_id_entry = tk.Entry(self.evaluate_rule_frame, width=50)
        self.mega_rule_id_entry.pack()
        tk.Label(self.evaluate_rule_frame, text="Data (JSON)").pack()
        self.data_entry = tk.Entry(self.evaluate_rule_frame, width=50)
        self.data_entry.pack()
        self.evaluate_rule_button = tk.Button(self.evaluate_rule_frame, text="Evaluate Rule", command=self.evaluate_rule)
        self.evaluate_rule_button.pack()

        # Modify Rule
        self.modify_rule_frame = tk.Frame(root)
        self.modify_rule_frame.pack(pady=10)
        tk.Label(self.modify_rule_frame, text="Modify Rule ID").pack()
        self.modify_rule_id_entry = tk.Entry(self.modify_rule_frame, width=50)
        self.modify_rule_id_entry.pack()
        tk.Label(self.modify_rule_frame, text="New Rule String").pack()
        self.new_rule_string_entry = tk.Entry(self.modify_rule_frame, width=50)
        self.new_rule_string_entry.pack()
        self.modify_rule_button = tk.Button(self.modify_rule_frame, text="Modify Rule", command=self.modify_rule)
        self.modify_rule_button.pack()

        # Output
        self.output_text = tk.Text(root, height=10, width=80)
        self.output_text.pack(pady=10)

    def create_rule(self):
        rule_string = self.rule_string_entry.get()
        try:
            response = requests.post(f"{BASE_URL}/create_rule", json={"rule_string": rule_string})
            response.raise_for_status()
            self.output_text.insert(tk.END, f"Create Rule Response: {response.json()}\n")
        except requests.exceptions.RequestException as e:
            self.output_text.insert(tk.END, f"Error: {e}\n")

    def combine_rules(self):
        rule_ids = self.rule_ids_entry.get().split(',')
        rule_ids = [int(id.strip()) for id in rule_ids]
        try:
            response = requests.post(f"{BASE_URL}/combine_rules", json={"rule_ids": rule_ids})
            response.raise_for_status()
            self.output_text.insert(tk.END, f"Combine Rules Response: {response.json()}\n")
        except requests.exceptions.RequestException as e:
            self.output_text.insert(tk.END, f"Error: {e}\n")

    def evaluate_rule(self):
        mega_rule_id = int(self.mega_rule_id_entry.get())
        data = self.data_entry.get()
        try:
            data_json = json.loads(data)
            response = requests.post(f"{BASE_URL}/evaluate_rule", json={"rule_id": mega_rule_id, "data": data_json})
            response.raise_for_status()
            self.output_text.insert(tk.END, f"Evaluate Rule Response: {response.json()}\n")
        except json.JSONDecodeError as e:
            self.output_text.insert(tk.END, f"JSON Decode Error: {e}\n")
        except requests.exceptions.RequestException as e:
            self.output_text.insert(tk.END, f"Error: {e}\n")

    def modify_rule(self):
        rule_id = int(self.modify_rule_id_entry.get())
        new_rule_string = self.new_rule_string_entry.get()
        try:
            response = requests.post(f"{BASE_URL}/modify_rule", json={"rule_id": rule_id, "new_rule_string": new_rule_string})
            response.raise_for_status()
            self.output_text.insert(tk.END, f"Modify Rule Response: {response.json()}\n")
        except requests.exceptions.RequestException as e:
            self.output_text.insert(tk.END, f"Error: {e}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = RuleEngineApp(root)
    root.mainloop()
