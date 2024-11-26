from zhipuai import ZhipuAI
from flask import Flask, render_template, request, jsonify

# 创建Flask实例
app = Flask(__name__)

# 创建ZhipuAI实例，并传入APIKey
client = ZhipuAI(api_key="5947c467381fbebbdb52372af7779960.BfqMTtsJAXW9neJi") # 请填写您自己的APIKey
clientc = ZhipuAI(api_key="fed76c71e516c486e1bcc058fc6bf4ca.Lni1nsQevsfJvVhG")

# 定义根路由，返回index.html页面
@app.route('/')
def home():
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
            {"role": "system", "content": "你的工作是接收来自用户的输入，如果用户输入的内容是他的经历就在这段经历的前面增加一个฿符号，如果输入的不是用户的经历，则输出“请输入您想要设计成徽章的事情”"},
            {"role": "user","content": user_input}
        ],
    )

    # 获取AI的回复
    ai_response = response.choices[0].message.content

    #检索“徽章设计方案”字样
    if "฿" in ai_response:
        #把设计方案转交至cogview
        responsec = clientc.images.generations(
        model="cogView-3-plus", #填写需要调用的模型编码
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