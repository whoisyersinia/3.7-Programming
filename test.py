class NPC:
    def __init__(self, name, dialogue_tree):
        self.name = name
        self.dialogue_tree = dialogue_tree

    def initiate_dialogue(self):
        print(f"{self.name}: Hello there!")
        current_node = self.dialogue_tree
        while True:
            if isinstance(current_node, dict):
                options = current_node.keys()
                print("Options:")
                for i, option in enumerate(options, 1):
                    print(f"{i}. {option}")
                print("0. Exit")
                user_choice = input("Your choice: ")
                if user_choice == "0":
                    print(f"{self.name}: Goodbye!")
                    break
                try:
                    index = int(user_choice) - 1
                    selected_option = list(options)[index]
                    print(selected_option)
                    current_node = current_node[selected_option]
                    if isinstance(current_node, str):
                        print(f"{self.name}: {current_node}")
                        current_node = self.dialogue_tree  # Reset to root after leaf node
                except (ValueError, IndexError):
                    print("Invalid choice. Please select again.")
            else:
                print(f"{self.name}: I don't understand that.")
                current_node = self.dialogue_tree  # Reset to root for invalid input

# Define dialogue trees for NPCs
bob_dialogue_tree = {
    "hi": "Hi there! How can I help you?",
    "how are you": "I'm doing well, thank you for asking.",
    "bye": "Goodbye! Come back anytime.",
    "services": {
        "What services do you offer?": {
            "repair": "We offer repair services for all sorts of equipment.",
            "sales": "We have a wide range of products available for sale.",
            "information": "We can provide information about our services and products.",
            "other": "Please specify what you're looking for."
        },
        "other": "I'm sorry, I didn't understand that. Would you like to ask something else?"
    }
}
alice_dialogue_tree = {
    "hello": "Hello, what can I do for you?",
    "how's it going": "I'm fine, thanks for asking.",
    "see you later": "Goodbye, take care!"
}

# Create NPCs
bob = NPC("Bob", bob_dialogue_tree)
alice = NPC("Alice", alice_dialogue_tree)

# Initiate dialogue
print("Conversation with Bob:")
bob.initiate_dialogue()

print("\nConversation with Alice:")
alice.initiate_dialogue()
