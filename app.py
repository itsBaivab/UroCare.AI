import chainlit as cl
import requests
API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/d30b1e8a5bd36620f3710b178f5f9673/ai/run/"
headers = {"Authorization": "Bearer Vb8tymIOp_0pJDawvLQ634Y_z7yzOvkzJumR1me7"}

def run(model, inputs):
    input_data = { "messages": inputs }
    try:
        response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input_data)
        response.raise_for_status()
        return response.json()["result"]["response"]
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return None

@cl.step
def tool(prompt):
    inputs = [
        { "role": "system", "content": "You are a Urologist Doctor who provides friendly assistance and helps to diagnose patients"  },
        { "role": "user", "content": prompt }
    ]
    return run("@cf/mistral/mistral-7b-instruct-v0.1", inputs)

@cl.on_message
async def main(message: cl.Message):
    user_input = message.content  # Get user input
    tool_response = tool(user_input)  # Pass user input as a prompt to the tool

    # Send the final answer or intermediate response from the tool.
    await cl.Message(content=tool_response).send()

