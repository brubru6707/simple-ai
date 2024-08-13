import pyperclip
import keyboard
import tkinter as tk
from tkinter import simpledialog, messagebox
import requests as req
import webbrowser
import threading
import queue
import json

def get_response(inquiry, highlighted_text, result_queue):
    url = 'https://ai-arsenal.vercel.app/api/gemai'
    db_url = 'http://127.0.0.1:5000/api/submit_question'
    try:
        ai_response = req.post(url, json={'question': inquiry + " " + highlighted_text}, timeout=5)
        print("this is working")
        print(ai_response.text)
        response_text = json.loads(ai_response.text)['text']
        try:
            response = req.post(db_url, json={'question': inquiry + " " + highlighted_text, 'response': response_text}, timeout=5)
            if response.status_code == 200:
                print("submit to the db")
                result = response.json().get('response', 'No response received')
            else:
                result = f"Failed to fetch data: {response.status_code}"
        except req.exceptions.RequestException as e:
            print(f"Request failed phase 2: {e}")
    except req.exceptions.RequestException as er:
        print(f"Request failed phase 1: {er}")
    
    result_queue.put(result)

def ask_inquiry_thread(highlighted_text, result_queue):
    inquiry = simpledialog.askstring("Gemini", "Inquiry: ")
    if inquiry:
        # Start the thread and pass the queue
        threading.Thread(target=get_response, args=(inquiry, highlighted_text, result_queue)).start()
        main_root.after(100, check_queue, result_queue)

def ask_inquiry(highlighted_text):
    result_queue = queue.Queue()
    main_root.after(0, ask_inquiry_thread, highlighted_text, result_queue)

def check_queue(result_queue):
    try:
        result = result_queue.get_nowait()  # Get the result without blocking
        show_response(result)
    except queue.Empty:
        # If no result yet, check again after some time
        main_root.after(100, check_queue, result_queue)

def show_response(response):
    messagebox.showinfo("Response", response)

def process_copied_text():
    ask_inquiry(pyperclip.paste())

def open_webpage():
    webbrowser.open("http://localhost:5000")

# Initialize the main Tkinter root
main_root = tk.Tk()
main_root.withdraw()  # Hide the main window

keyboard.add_hotkey('ctrl+alt+end', process_copied_text)
keyboard.add_hotkey("Ctrl+Alt+Down Arrow", open_webpage)

# Start the Tkinter main loop
main_root.mainloop()
