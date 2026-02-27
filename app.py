
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 用于session管理
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# -------------------------- 数据库模块（分模块+索引优化） --------------------------
# 1. 用户模块
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False, index=True)  # 索引优化
    password_hash = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), default='user')  # 'user' 或 'admin'
    is_approved = db.Column(db.Boolean, default=False)  # 注册审批状态

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# 2. 登录日志模块
class LoginLog(db.Model):
    __tablename__ = 'login_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)  # 索引优化
    login_time = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(20))

# 3. 内容管理模块
class Content(db.Model):
    __tablename__ = 'contents'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, index=True)  # 索引优化
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    publish_time = db.Column(db.DateTime, default=datetime.utcnow)

# -------------------------- 普通用户功能：登录/注册 --------------------------
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"code": 1, "msg": "用户名已存在"}), 400
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"code": 0, "msg": "注册成功，请等待管理员审批"})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']) and user.is_approved:
        session['user_id'] = user.id
        log = LoginLog(user_id=user.id, ip_address=request.remote_addr)
        db.session.add(log)
        db.session.commit()
        return jsonify({"code": 0, "msg": "登录成功", "role": user.role})
    return jsonify({"code": 1, "msg": "用户名/密码错误或账号未审批"}), 401

# -------------------------- 管理员功能：审批/日志/内容管理 --------------------------
@app.route('/api/admin/approve/<int:user_id>', methods=['POST'])
def approve_user(user_id):
    if 'user_id' not in session or User.query.get(session['user_id']).role != 'admin':
        return jsonify({"code": 1, "msg": "无权限"}), 403
    user = User.query.get(user_id)
    user.is_approved = True
    db.session.commit()
    return jsonify({"code": 0, "msg": "审批通过"})

@app.route('/api/admin/users', methods=['GET'])
def admin_get_users():
    if 'user_id' not in session or User.query.get(session['user_id']).role != 'admin':
        return jsonify({"code": 1, "msg": "无权限"}), 403
    users = User.query.all()
    return jsonify({
        "code": 0,
        "data": [{"id": u.id, "username": u.username, "role": u.role, "is_approved": u.is_approved} for u in users]
    })

@app.route('/api/admin/login-logs', methods=['GET'])
def admin_get_login_logs():
    if 'user_id' not in session or User.query.get(session['user_id']).role != 'admin':
        return jsonify({"code": 1, "msg": "无权限"}), 403
    logs = LoginLog.query.all()
    return jsonify({
        "code": 0,
        "data": [{"id": l.id, "user_id": l.user_id, "login_time": l.login_time, "ip": l.ip_address} for l in logs]
    })

@app.route('/api/admin/content', methods=['POST'])
def admin_add_content():
    if 'user_id' not in session or User.query.get(session['user_id']).role != 'admin':
        return jsonify({"code": 1, "msg": "无权限"}), 403
    data = request.json
    content = Content(title=data['title'], content=data['content'], author_id=session['user_id'])
    db.session.add(content)
    db.session.commit()
    return jsonify({"code": 0, "msg": "内容发布成功"})

# -------------------------- 页面路由 --------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin_page():
    if 'user_id' not in session or User.query.get(session['user_id']).role != 'admin':
        return redirect(url_for('login_page'))
    return render_template('admin.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

# -------------------------- 初始化数据库 --------------------------
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', role='admin', is_approved=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
