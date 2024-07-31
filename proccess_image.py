import pyperclip  # Used to check what is copied
import keyboard  # Adds keyboard bindings
import tkinter as tk
from tkinter import simpledialog  # Dialog box for input
from tkinter import messagebox  # Message box
import google.generativeai as genai  # AI

# Configure the Generative AI with your API key
genai.configure(api_key="")
model = genai.GenerativeModel('gemini-1.5-flash')

def get_response(inquiry, highlighted_text):
    try:
        response = model.generate_content(inquiry + highlighted_text)
        return response.text
    except Exception as e:
        return f"Error: {e}"

def show_response(response):
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    messagebox.showinfo("Response", response)
    root.destroy()

def ask_inquiry(highlighted_text):
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    root.focus_set()
    user_input = simpledialog.askstring("Gemini", "Inquiry: ")
    root.destroy()
    if user_input is not None:
        response = get_response(user_input, highlighted_text)
        show_response(response)

def process_copied_text():
    # Get the text from the clipboard
    highlighted_text = pyperclip.paste()
    # Process the highlighted text
    ask_inquiry(highlighted_text)

def set_up_proccess_image_function():
    keyboard.add_hotkey('ctrl+b', process_copied_text)
    keyboard.wait('ctrl+esc')
