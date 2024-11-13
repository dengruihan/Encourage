from zhipuai import ZhipuAI
from flask import Flask, render_template, request, jsonify

# 创建Flask实例
app = Flask(__name__)

# 创建ZhipuAI实例，并传入APIKey
client = ZhipuAI(api_key="5947c467381fbebbdb52372af7779960.BfqMTtsJAXW9neJi") # 请填写您自己的APIKey

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
            {"role": "system", "content": "你是一台先进的AI勋章设计助手，专长于根据用户的个人经历和成就，创造性地设计勋章。你的任务是倾听用户的经历描述，分析其中的关键信息。最后从画面元素/画面底色 三个角度输出设计方案。你需要在你的设计方案前加上‘徽章设计方案1’字样"},
            {"role": "user","content": user_input}
        ],
    )

    # 获取AI的回复
    ai_response = response.choices[0].message.content

    #检索“徽章设计方案”字样
    if "1" in ai_response:
        #把设计方案转交至cogview
        clientc = ZhipuAI(api_key="fed76c71e516c486e1bcc058fc6bf4ca.Lni1nsQevsfJvVhG")
        responsec = client.images.generations(
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