def chatbot_response(user_input):
    user_input = user_input.lower()  # Convert input to lowercase for easier matching

    if "hello" in user_input or "hi" in user_input:
        return "Hello! I am your friendly chatbot. How can I assist you today?"
    elif "how are you" in user_input:
        return "I'm just a chatbot, I am alway fine as I am powered by your computer"
    elif "bye" in user_input or "goodbye" in user_input:
        return "Goodbye! Have a great day!"
    elif "your name" in user_input:
        return "I'm a Akash, your friendly chatbot, here to assist you!"
    else:
        return "I'm not sure how to respond to that. Can you greet me only 'hello','how are you','your name' and 'bye' please?"

# Run the chatbot in a loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["bye", "exit", "quit"]:
        print("Akash: Goodbye!")
        break
    response = chatbot_response(user_input)
    print(f"Akash: {response}")
