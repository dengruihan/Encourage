from zhipuai import ZhipuAI
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext
from sqlalchemy import Column, String
import os

# 创建Flask实例
app = Flask(__name__)
app.secret_key = os.urandom(24)  # 用于保护会话安全
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your-database.db'
db = SQLAlchemy(app)

# 创建一个CryptContext实例
pwd_context = CryptContext(schemes=["pbkdf2_sha256", "argon2"], deprecated="auto")

# 定义用户模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

# 创建数据库和表
with app.app_context():
    db.create_all()
    # 如果user表不存在password_hash字段，添加该字段
    if not hasattr(User, 'password_hash'):
        db.session.execute('ALTER TABLE user ADD COLUMN password_hash VARCHAR(128)')
        db.session.commit()

# 注册视图
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 使用CryptContext实例的hash方法来生成密码的哈希值
        password_hash = pwd_context.hash(password)
        new_user = User(username=username, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

# 登录视图
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        # 使用CryptContext实例的verify方法来验证密码
        if user and pwd_context.verify(password, user.password_hash):
            session['username'] = username
            return redirect(url_for('homecheck'))
        else:
            # 处理登录失败的情况
            pass
    return render_template('login.html')

# 创建ZhipuAI实例，并传入APIKey
client = ZhipuAI(api_key="5947c467381fbebbdb52372af7779960.BfqMTtsJAXW9neJi")  # 请填写您自己的APIKey
clientc = ZhipuAI(api_key="fed76c71e516c486e1bcc058fc6bf4ca.Lni1nsQevsfJvVhG")

# 定义根路由，返回index.html页面
@app.route('/')
def home():
    return render_template('login.html')

# 更新主页路由以检查用户是否已登录
@app.route('/homecheck')
def homecheck():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

# 定义chat路由，接收POST请求，并返回json格式的响应
@app.route('/chat', methods=['POST'])
def chat():
    # 获取表单中的输入
    user_input = request.form.get('input')
    # 调用ZhipuAI的chat.completions.create方法，传入模型名称和输入
    response = client.chat.completions.create(
        model="glm-4-flash",  # 填写需要调用的模型名称
        messages=[
            {"role": "system", "content": "你的工作是接收来自用户的输入，如果用户输入的内容是他的经历就在这段经历的前面增加“฿设计徽章：”字符，如果输入的不是用户的经历，则输出“请输入您想要设计成徽章的事情”"},
            {"role": "user", "content": user_input}
        ],
    )

    # 获取AI的回复
    ai_response = response.choices[0].message.content

    # 检索“徽章设计方案”字样
    if "฿" in ai_response:
        # 把设计方案转交至cogview
        responsec = clientc.images.generations(
            model="cogView-3-plus",  # 填写需要调用的模型编码
            prompt=ai_response,
            size="1024x1024"
        )
        image_url = responsec.data[0].url

        # 返回JSON格式的AI响应和图片链接
        return jsonify(image_url)

    else:
        # 删除所有'\n'字符
        ai_response = ai_response.replace('\n', '')

        # 返回JSON格式的AI响应
        return jsonify(ai_response)

# 启动Flask实例
if __name__ == '__main__':
    app.run(debug=True)
