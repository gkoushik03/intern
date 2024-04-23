from transformers import GPT2LMHeadModel, GPT2Tokenizer
import requests
import sqlite3

# Load pretrained GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Initialize SQLite database connection
conn = sqlite3.connect('chatbot_db.sqlite')
c = conn.cursor()

# Create table to store general information
c.execute('''CREATE TABLE IF NOT EXISTS general_info
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              category TEXT,
              question TEXT,
              answer TEXT)''')

# Populate the table with some general information (you can add more)
general_info_data = [
    ('general', 'what is your name', 'I am Koushikchat, our virtual assistant.'),
    ('general', 'how are you', 'I\'m just a koushikbot, but I\'m here to help Koushik!'),
    ('general', 'who created you', 'I was created by a Koushik.'),
    ('general','what is lifespan','until power is on')
]
c.executemany('INSERT INTO general_info (category, question, answer) VALUES (?, ?, ?)', general_info_data)
conn.commit()

# Define function to generate response using GPT-2 model
def generate_response(user_input, max_length=100):
    input_ids = tokenizer.encode(user_input, return_tensors="pt")
    response_ids = model.generate(input_ids, max_length=max_length, num_return_sequences=1)
    response = tokenizer.decode(response_ids[0], skip_special_tokens=True)
    return response

# Define function to retrieve general information from the database
def get_general_info(question):
    c.execute('SELECT answer FROM general_info WHERE question LIKE ?', ('%' + question + '%',))
    result = c.fetchone()
    return result[0] if result else None

# Main function to interact with the chatbot
def chat_with_bot():
    print("Welcome to the ChatBot. Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        else:
            # Example of intent classification and response generation
            if "bitcoin" in user_input.lower() or "btc" in user_input.lower():
                response = get_bitcoin_info()
            else:
                # Try to retrieve general information from the database
                response = get_general_info(user_input)
                if not response:
                    # If no relevant information found, generate response using GPT-2 model
                    response = generate_response(user_input)
            print("ChatBot:", response)

# Main function
if __name__ == "__main__":
    chat_with_bot()

# Close database connection when done
conn.close()
