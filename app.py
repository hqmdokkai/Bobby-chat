from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = '7x2mxTlL4aONKLM1nygDNNk2Wfnk31at'

users_file = 'users.txt'
messages_file = 'messages.txt'

def save_user(username, password):
    with open(users_file, 'a') as f:
        f.write(f'{username}:{password}\n')

def check_user(username, password):
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            for line in f:
                user, passw = line.strip().split(':')
                if user == username and passw == password:
                    return True
    return False

def user_exists(username):
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            for line in f:
                user, _ = line.strip().split(':')
                if user == username:
                    return True
    return False

def save_message(sender, recipient, message):
    with open(messages_file, 'a') as f:
        f.write(f'{sender}:{recipient}:{message}\n')

def load_messages_for_user(username):
    messages_list = []
    if os.path.exists(messages_file):
        with open(messages_file, 'r') as f:
            for line in f:
                sender, recipient, message = line.strip().split(':')
                if sender == username or recipient == username:
                    display_message = f'{"You" if sender == username else sender} to {"You" if recipient == username else recipient}: {message}'
                    messages_list.append(display_message)
    return messages_list

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('chat'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_user(username, password):
            session['username'] = username
            return redirect(url_for('chat'))
        return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_exists(username):
            return render_template('register.html', error='Username already exists')
        save_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    if request.method == 'POST':
        recipient = request.form['recipient']
        message = request.form['message']
        save_message(username, recipient, message)
    messages_list = load_messages_for_user(username)
    return render_template('chat.html', username=username, messages=messages_list)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=False)
