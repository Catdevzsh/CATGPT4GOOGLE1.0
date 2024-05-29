import tkinter as tk
from tkinter import scrolledtext
import json

import requests

class ChatApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("$CATGPT 1.1 [C] Flames AI")
        self.geometry("800x600")
        self.resizable(False, False)
        self.create_widgets()
        self.init_chat_history()

    def create_widgets(self):
        # Output text area (scrolled text for better control over scrolling)
        self.output_text = scrolledtext.ScrolledText(self, state="disabled", wrap=tk.WORD)
        self.output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Input area (simple text area for user input)
        self.input_text = tk.Text(self, height=3)
        self.input_text.pack(fill=tk.X, padx=10, pady=(0, 10))

        # Send button
        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.pack(pady=(0, 10))

    def init_chat_history(self):
        # Initialize the chat history with a friendly message
        self.update_output_text("CATGPT: Hello! I'm CATGPT. Share your prompt, and I'll generate a response showcasing my capabilities!\n\n")

    def send_message(self):
        # Get the user's message from the input text area
        user_message = self.input_text.get("1.0", tk.END).strip()
        self.input_text.delete("1.0", tk.END)

        if user_message:
            self.update_output_text(f"User: {user_message}\n")

            # Construct the API request to the Gemini API
            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent"
            headers = {'Content-Type': 'application/json'}
            params = {'key': '# INSERT YOUR API KEY'}
            data = {'contents': [{'parts': [{'text': user_message}]}]}

            try:
                response = requests.post(url, headers=headers, json=data, params=params)
                response_data = response.json()
                
                # Parse the response and extract the AI's message
                ai_response = response_data['candidates'][0]['content']
                self.update_output_text(f"CATGPT: {ai_response}\n\n")
            except Exception as e:
                self.update_output_text(f"Error: {str(e)}\n\n")

    def update_output_text(self, message):
        # Update the output text area with new message
        self.output_text.config(state="normal")
        self.output_text.insert(tk.END, message)
        self.output_text.config(state="disabled")
        self.output_text.see(tk.END)

if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()
