import openai
import json
import os

#open ai api key here

openai.api_key = "your_api_key_here"


memory_file = "ai_memory.json"
if os.path.exists(memory_file):
    with open(memory_file, "r") as file:
        memory = json.load(file)
else:
    memory = {}

def save_memory():
    with open(memory_file, "w" ) as file:
        json.dump(memory, file, indent = 4)

def search_memory(question):
    return memory.get(question.lower())


def learn_from_user(question):
    print("I don't know the answer yet. Can you teach me?")
    user_answer = input("your answer: ")
    memory[question.lower()] = user_answer
    save_memory()
    print("thanks")
    return user_answer

def ai_generate_answer(question):
    prompt = f"Answer this question using common knowledge and web search: {question}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or gpt-4 if you have access
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.7
    )
    return response['choices'][0]['message']['content'].strip()

def ai_brain():
        print("Hello! I'm your smart Meta AI Assistant.")
        print("I learn from users, and use AI to help you. Ask me anything!")
        print("Type 'exit' to quit.\n")

        while True:
            user_input = input("You: ").strip()
            if user_input.lower() == "exit":
                print("Bye! Remember, I'm always learning.")
                break

            known_answer = search_memory(user_input)
            if known_answer:
                print("📚 From memory:", known_answer)
            else:
                print("🔍 Thinking...")
                try:
                    ai_answer = ai_generate_answer(user_input)
                    print("🤖 AI Answer:", ai_answer)
                    feedback = input("Was this answer helpful? (yes/no): ").lower()
                    if feedback == "no":
                        ai_answer = learn_from_user(user_input)
                    else:
                        memory[user_input.lower()] = ai_answer
                        save_memory()
                except Exception as e:
                    print("⚠️ Error using AI:", e)
                    fallback = learn_from_user(user_input)

# Start the assistant
ai_brain()
