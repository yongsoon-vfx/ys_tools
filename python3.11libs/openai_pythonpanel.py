import sys

import google.generativeai as genai
import markdown  # For converting Markdown to HTML
from PySide2.QtWidgets import (
    QApplication,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

# Set your Google API key here
genai.configure(api_key="AIzaSyDb0uKI3Z4PWrgRgtqyRVQvhWicK5euvvU")


class ChatBox(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Chat with Gemini")

        # Create a vertical layout
        layout = QVBoxLayout()

        # Create a text area to display the conversation
        self.conversation = QTextEdit()
        self.conversation.setReadOnly(True)
        layout.addWidget(self.conversation)

        # Create a text input field
        self.input_field = QLineEdit()
        layout.addWidget(self.input_field)

        # Create a send button
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        layout.addWidget(self.send_button)

        # Set the layout for the main window
        self.setLayout(layout)

        # Initialize the Gemini model
        self.model = genai.GenerativeModel("gemini-2.0-flash-lite")

    def send_message(self):
        # Get the user's message
        user_message = self.input_field.text()
        self.input_field.clear()

        # Display the user's message in the conversation area
        self.conversation.append(f"<b>You:</b> {user_message}")

        # Send the message to the Gemini API
        response = self.get_gemini_response(user_message)

        # Convert the response (Markdown) to HTML
        response_html = self.markdown_to_html(response)

        # Display Gemini's response in the conversation area
        self.conversation.append(f"<b>Gemini:</b> {response_html}")

    def get_gemini_response(self, message):
        # Use the Gemini API to get a response
        response = self.model.generate_content(message)

        # Extract and return the response text
        return response.text

    def markdown_to_html(self, markdown_text):
        # Convert Markdown to HTML
        html = markdown.markdown(markdown_text)
        return html


def createInterface():
    return ChatBox()
