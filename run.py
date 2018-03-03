import os
from datetime import datetime #python module that will timestamp messages
from flask import Flask, redirect, render_template, request #redirect to redirect the messages to the list

app = Flask(__name__)
#messages = [] #chat items stored in a list. Now removed as we are using a dictionary

def write_to_file(filename, data):
    """Handle the process of writing data to a text file"""
    with open(filename, "a") as file:
        file.writelines(data)

def add_messages(username, message):
    # Add messages in to the 'messages' text file 
    write_to_file("data/messages.txt", "({0}) {1} - {2}\n".format(
            datetime.now().strftime("%H:%M:%S"),#Timestamp time order 
            username.title(), 
            message))

def get_all_messages():
    """Get all of the messages and separate them using a 'br'"""
    messages = []
    with open("data/messages.txt", "r") as chat_messages:
        messages = chat_messages.readlines()
    return messages #when the serer is stopped, the messages are saved to this txt file so when rebooted the messages are not lost ajd the user will see their message history on si

@app.route('/', methods = ["GET", "POST"])
def index():
    """Main page with instructions"""
    
    #Handle POST request
    if request.method == "POST":
        write_to_file("data/users.tst", request.form["username"] + "\n") #opening the users.txt file and writing to it
        return redirect(request.form["username"]) #upon submit, the index page is shown with username submitted
    return render_template("index.html")
    
@app.route('/<username>')
def user(username):
    """Display chat messages"""
    messages = get_all_messages()
    return render_template("chat.html", username=username, chat_messages=messages)
    
@app.route('/<username>/<message>')
def send_message(username, message):
    """Create a new message and redirect back to the chat page"""
    add_messages(username, message)
    return redirect(username)
    
    
app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)