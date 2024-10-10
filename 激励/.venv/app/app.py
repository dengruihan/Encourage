from flask import Flask, request, redirect, render_template, session, url_for
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于加密会话

# 假设这是我们的用户数据库
users = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return "用户名已存在，请更改名字。"
        else:
            users[username] = password
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('random_page'))
        elif username not in users:
            # 用户名不在数据库中，提示是否是新用户
            return render_template('new_user.html', username=username)
        else:
            return "用户名或密码错误，请修改。"
    return render_template('login.html')

@app.route('/random_page')
def random_page():
    if 'username' in session:
        # 这里只是一个示例，实际应用中可以指向真正的随机网页
        random_urls = ['https://www.example1.com', 'https://www.example2.com', 'https://www.example3.com']
        return redirect(random.choice(random_urls))
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
