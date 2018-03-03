import os
from datetime import datetime #python module that will timestamp messages
from flask import Flask, redirect, render_template, request #redirect to redirect the messages to the list

app = Flask(__name__)
messages = [] #chat items stored in a list

def add_messages(username, message):
    # Add messages in to the messages list
    now = datetime.now().strftime("%H:%M:%S") #Timestamp time order
    messages_dict = {"timestamp": now, "from": username, "message": message}
    messages.append(messages_dict)
    #messages.append("({}) {}: {}".format(now, username, message)) #brackets act as placeholders for time, user and message

def get_all_messages():
    """Get all of the messages and separate them using a 'br'"""
    return messages #Now we are using a dictionary we only need them returned.

@app.route('/', methods = ["GET", "POST"])
def index():
    """Main page with instructions"""
    if request.method == "POST":
        with open("data/users.txt", "a") as user_list:
            user_list.writelines(request.form["username"] + "\n") #opening the users.txt file and writing to it
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