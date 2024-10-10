from flask import Flask, request, redirect, render_template, session, url_for, flash
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
            flash('用户名已存在，请更改名字。')
        else:
            users[username] = password
            flash('注册成功，请登录。')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # 检查用户是否输入了账户和密码
        if not username or not password:
            flash('错误：账户和密码不能为空，请填写后再尝试登录！')
            return redirect(url_for('login'))

        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('home'))  # 修改这里，重定向到新主页
        elif username not in users:
            # 用户名不在数据库中，提示是否是新用户
            flash('用户名不存在，请注册。')
            return redirect(url_for('register'))
        else:
            flash('用户名或密码错误，请修改。')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/home')
def home():
    if 'username' in session:
        # 用户已登录，显示主界面
        return render_template('home.html')
    else:
        # 用户未登录，重定向到登录页面
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
