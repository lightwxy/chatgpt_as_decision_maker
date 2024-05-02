from openai import OpenAI
client = OpenAI()
import time
import os

from example_data import supplier_id
from example_data import supplier_data_1 as supplier_data
from dimensions import dimensions

# API key configuration (ensure to configure this securely)
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")



def construct_prompt(supplier_id):
    prompt = f"You are an expert in the field of supply chain, possessing the ability to provide honest and scientific evaluations of supplier’s delivery capability and product quality within the supply chain. Now, you are required to assess the quality level of a supplier based on four dimensions and 16 criteria. Each dimension and the criteria within them have their respective importance weights, \
    The supplier’s quality level is to be determined on a scale of good, average or poor, across these dimensions and criteria. Now please assessing supplier {supplier_id}.\n"
    for dim_name, dim_info in dimensions.items():
        prompt += f"\nDimension: {dim_name} (Weight: {dim_info['weight']}%)\n"
        for crit_name, crit_weight in dim_info['criteria'].items():
            prompt += f"- Criteria: {crit_name}, Weight: {crit_weight}%, Record: {supplier_data[crit_name]}\n"

    prompt += "\nPlease provide evaluation levels for each dimension and criterion according to the following template, and provide the supplier's final evaluation level on a scale of good, average, or poor with json format:\n"
    return prompt

def query_chatgpt(prompt):
    while True:
        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": prompt}],
                temperature=0
            )
            response_text = completion.choices[0].message.content
            return response_text
        except Exception as e:
            print(f"Error occurred: {e}. Retrying in 1 second...")
            time.sleep(1)

# Example usage
prompt = construct_prompt(supplier_id)
print(prompt)
result = query_chatgpt(prompt)
print(result)

# 以下是返回的结果
'''
{
  "Supplier123": {
    "Quality Assurance": {
      "Product Acceptance Rate": "Average",
      "Concession Acceptance Rate": "Average",
      "Rework and Return Cases": "Average",
      "Outsourcing Review": "Average",
      "Quality Issues": "Average"
    },
    "Production and Supply": {
      "Timeliness of Delivery": "Average",
      "Production Process": "Average"
    },
    "Cost Control": {
      "Product Price": "Average",
      "Transportation Cost": "Poor",
      "After-Sales Service Cost": "Average",
      "Minimum Order Quantity Requirement": "Poor"
    },
    "Service Capability": {
      "Response Speed": "Average",
      "Communication Level": "Average",
      "Service System Integrity": "Average",
      "Spare Parts Availability": "Average",
      "Product Maintainability": "Average"
    },
    "Final Evaluation": "Average"
  }
}

'''
