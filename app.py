
from flask import Flask, jsonify, request, send_from_directory
from datetime import datetime
from flask_cors import CORS  # 保留跨域支持

# 初始化Flask应用，指定当前目录为静态文件目录（用于加载前端页面）
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # 允许跨域，确保前端能正常调用

# ==========================
# 新增：前端请求侦探（核心功能）
# ==========================
@app.before_request
def log_request_info():
    """每次前端发请求，都会在IDLE里打印出请求的地址和方式"""
    print(f"\n【前端发起了请求】")
    print(f"请求方式: {request.method}")
    print(f"请求地址: {request.path}")
    print(f"请求数据: {request.get_data(as_text=True)[:200]}")  # 只显示前200个字符
    print("-" * 50)

# ==========================
# 内存数据库（数据临时存储）
# ==========================
users = {}
career_plans = {}
login_logs = []

# ==========================
# 后端接口（目前是我们之前约定的地址，运行后根据打印结果修改）
# ==========================

@app.route('/register', methods=['POST'])
def register():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"msg": "用户名和密码不能为空", "code": 400}), 400
    
    if username in users:
        return jsonify({"msg": "用户名已存在", "code": 400}), 400
    
    users[username] = {
        "password": password,
        "email": data.get('email', ''),
        "register_time": datetime.now().isoformat(),
        "last_login_ip": None,
        "last_login_time": None
    }
    return jsonify({"msg": "注册成功", "code": 200}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')
    
    if username not in users or users[username]['password'] != password:
        return jsonify({"msg": "用户名或密码错误", "code": 401}), 401
    
    # 记录登录日志
    login_logs.append({
        "username": username,
        "login_time": datetime.now().isoformat(),
        "ip": request.remote_addr
    })
    
    # 更新用户最后登录信息
    users[username]['last_login_ip'] = request.remote_addr
    users[username]['last_login_time'] = datetime.now().isoformat()
    
    return jsonify({
        "msg": "登录成功", 
        "code": 200,
        "data": {"username": username}
    }), 200

@app.route('/admin/login_logs', methods=['GET'])
def get_login_logs():
    return jsonify({
        "msg": "获取成功",
        "code": 200,
        "data": login_logs
    }), 200

@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    data = request.json or {}
    username = data.get('username')
    
    if not username or username not in users:
        return jsonify({"msg": "用户不存在", "code": 404}), 404
    
    # 结合民航+会计专业生成规划
    plan = f"""为{username}定制的民航财会职业规划：
1. 学业阶段：考取CPA核心科目，重点学习航空运输企业会计核算；
2. 实习阶段：优先投递航司财务部、机场集团计财部或民航业会计师事务所；
3. 职业发展：初级可从事成本核算、营收审计，资深后向民航财务管理专家方向晋升。"""
    
    career_plans[username] = {
        "plan": plan,
        "created_at": datetime.now().isoformat()
    }
    
    return jsonify({
        "msg": "规划生成成功",
        "code": 200,
        "data": career_plans[username]
    }), 200

# ==========================
# 主页入口
# ==========================
@app.route('/')
def index():
    return send_from_directory('.', '主页.html')

# ==========================
# 启动服务
# ==========================
if __name__ == '__main__':
    app.run(debug=True, port=5000)
