from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于会话和flash消息

# 用于存储用户名和密码的简单字典（实际应用中应使用数据库）
users = {}

# 定义一个路由，用于处理用户登录请求
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 检查用户名和密码是否匹配
        if username in users and users[username] == password:
            flash('登录成功！', 'success')
            return redirect(url_for('index'))  # 登录成功后重定向到首页
        else:
            flash('用户名或密码错误，请重新输入！', 'danger')

    return render_template('login.html')

# 定义一个路由，用于处理用户注册请求
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 检查用户名是否已存在
        if username in users:
            flash('用户名已存在，请选择其他用户名！', 'danger')
        else:
            users[username] = password  # 将新用户添加到字典中
            flash('注册成功！', 'success')
            return redirect(url_for('login'))  # 注册成功后重定向到登录页面

    return render_template('register.html')

# 定义一个路由，用于显示首页
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
