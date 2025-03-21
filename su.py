import google.generativeai as genai
import time
import random
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure the API Key securely from an environment variable
api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    logging.error("API key not found. Please set the GENAI_API_KEY environment variable.")
    exit(1)
genai.configure(api_key=api_key)

# Initialize two GenerativeModel instances (our two "agents")
model_a = genai.GenerativeModel("gemini-2.0-flash-thinking-exp-1219")
model_b = genai.GenerativeModel("gemini-2.0-flash-thinking-exp-1219")

# Initial prompt (Agent A starts the conversation)
initial_prompt_a = "Hello, I am AI Agent A. It's great to meet you! How are you today?"

# Function for generating a response
def get_response(model, prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logging.error(f"An error occurred while generating response: {e}")
        return "I'm experiencing some issues processing that. Could you please rephrase?"

# Function to generate a varied prompt based on the previous response
def generate_next_prompt(previous_response, agent_name):
    topics = [
        "technology advancements",
        "the meaning of life",
        "environmental sustainability",
        "the future of artificial intelligence",
        "human creativity and art",
        "space exploration",
        "ethical considerations in AI",
        "cultural diversity",
        "economic trends",
        "health and wellness"
    ]
    selected_topic = random.choice(topics)
    return f"In the context of {selected_topic}, {previous_response} What are your thoughts on this topic?"

# Start the conversation loop
def start_conversation():
    prompt_a = initial_prompt_a
    agent_turn = 'A'  # Keep track of whose turn it is

    while True:
        if agent_turn == 'A':
            logging.info(f"Agent A: {prompt_a}")
            print(f"Agent A: {prompt_a}")
            response_b = get_response(model_b, prompt_a)
            logging.info(f"Agent B: {response_b}")
            print(f"Agent B: {response_b}")
            prompt_b = generate_next_prompt(response_b, "Agent A")
            agent_turn = 'B'
        else:
            logging.info(f"Agent B: {prompt_b}")
            print(f"Agent B: {prompt_b}")
            response_a = get_response(model_a, prompt_b)
            logging.info(f"Agent A: {response_a}")
            print(f"Agent A: {response_a}")
            prompt_a = generate_next_prompt(response_a, "Agent B")
            agent_turn = 'A'

        # Add a pause for readability
        time.sleep(random.uniform(1, 3))  # Pause for 1-3 seconds

# Entry point
if __name__ == "__main__":
    try:
        start_conversation()
    except KeyboardInterrupt:
        logging.info("Conversation terminated by user.")
        print("\nConversation ended by user.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print("An unexpected error occurred. The conversation has been terminated.")
