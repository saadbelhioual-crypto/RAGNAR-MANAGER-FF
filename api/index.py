import json
import hashlib
import os
import uuid
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler
import urllib.parse

DATA_PATH = '/tmp/data/'
USERS_FILE = DATA_PATH + 'users.json'
KEYS_FILE = DATA_PATH + 'keys.json'
TOKEN_FILE = DATA_PATH + 'amine_token.txt'

os.makedirs(DATA_PATH, exist_ok=True)

def init_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump({
                "RAGNAR": {
                    "password": hashlib.sha256("RAGNAR-TOP-1".encode()).hexdigest(),
                    "role": "admin",
                    "created": str(datetime.now()),
                    "keys_created": []
                }
            }, f)
    
    if not os.path.exists(KEYS_FILE):
        with open(KEYS_FILE, 'w') as f:
            json.dump({}, f)
    
    if not os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'w') as f:
            json.dump({}, f)

def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

def check_key_valid(key):
    with open(KEYS_FILE, 'r') as f:
        keys = json.load(f)
    
    if key not in keys:
        return False, "مفتاح غير صالح"
    
    expiry = datetime.fromisoformat(keys[key]['expiry'])
    if expiry < datetime.now():
        return False, "المفتاح منتهي الصلاحية"
    
    days_left = (expiry - datetime.now()).days
    return True, f"المفتاح صالح - متبقي {days_left} يوم"

def get_remaining_days(key):
    with open(KEYS_FILE, 'r') as f:
        keys = json.load(f)
    
    if key not in keys:
        return 0
    
    expiry = datetime.fromisoformat(keys[key]['expiry'])
    days_left = (expiry - datetime.now()).days
    return max(0, days_left)

HTML_LOGIN = '''<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TCP BOT - RAGNAR SYSTEM</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            min-height: 100vh;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a0033 50%, #000000 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .login-container {
            background: rgba(0, 0, 0, 0.85);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            width: 400px;
            box-shadow: 0 0 50px rgba(128, 0, 255, 0.3);
            border: 1px solid rgba(255,255,255,0.1);
        }
        h1 { text-align: center; color: #ff6600; margin-bottom: 10px; font-size: 28px; text-shadow: 0 0 10px rgba(255,102,0,0.5); }
        .subtitle { text-align: center; color: #9b59b6; margin-bottom: 30px; font-size: 14px; }
        input {
            width: 100%; padding: 12px 15px; margin: 10px 0;
            background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.2);
            border-radius: 10px; color: white; font-size: 16px;
            transition: all 0.3s;
        }
        input:focus { outline: none; border-color: #ff6600; box-shadow: 0 0 15px rgba(255,102,0,0.3); }
        button {
            width: 100%; padding: 12px; margin-top: 20px;
            background: linear-gradient(90deg, #ff6600, #9b59b6);
            border: none; border-radius: 10px; color: white; font-size: 18px;
            font-weight: bold; cursor: pointer; transition: transform 0.3s;
        }
        button:hover { transform: scale(1.02); }
        .toggle { text-align: center; margin-top: 20px; color: #888; cursor: pointer; }
        .toggle span { color: #ff6600; }
        .error { background: rgba(255,0,0,0.2); border: 1px solid red; border-radius: 10px; padding: 10px; margin-top: 15px; text-align: center; color: #ff4444; font-size: 14px; }
        .success { background: rgba(0,255,0,0.2); border: 1px solid green; border-radius: 10px; padding: 10px; margin-top: 15px; text-align: center; color: #00ff00; font-size: 14px; }
        .logo { text-align: center; margin-bottom: 20px; }
        .logo span { font-size: 50px; }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo"><span>👹</span></div>
        <h1>TCP BOT SYSTEM</h1>
        <div class="subtitle">POWERED BY RAGNAR</div>
        <form id="loginForm">
            <input type="text" id="username" placeholder="اسم المستخدم" required>
            <input type="password" id="password" placeholder="كلمة المرور" required>
            <button type="submit">دخول</button>
        </form>
        <div class="toggle" onclick="showRegister()">ليس لديك حساب؟ <span>إنشاء حساب جديد</span></div>
        <div id="message"></div>
    </div>
    <script>
        async function login() {
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const response = await fetch('/api/index.py?action=login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username, password, action: 'login'})
            });
            const data = await response.json();
            if (data.success) {
                localStorage.setItem('token', data.token);
                localStorage.setItem('username', username);
                localStorage.setItem('role', data.role);
                window.location.href = data.role === 'admin' ? '/admin' : '/dashboard';
            } else {
                document.getElementById('message').innerHTML = '<div class="error">' + data.error + '</div>';
            }
        }
        async function register() {
            const username = document.getElementById('reg-username').value;
            const password = document.getElementById('reg-password').value;
            const key = document.getElementById('reg-key').value;
            const response = await fetch('/api/index.py?action=register', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username, password, key, action: 'register'})
            });
            const data = await response.json();
            if (data.success) {
                document.getElementById('message').innerHTML = '<div class="success">تم إنشاء الحساب بنجاح!</div>';
                setTimeout(() => showLogin(), 2000);
            } else {
                document.getElementById('message').innerHTML = '<div class="error">' + data.error + '</div>';
            }
        }
        function showRegister() {
            document.querySelector('.login-container').innerHTML = `
                <div class="logo"><span>🔑</span></div>
                <h1>إنشاء حساب</h1>
                <div class="subtitle">أدخل مفتاح التفعيل</div>
                <form id="registerForm">
                    <input type="text" id="reg-username" placeholder="اسم المستخدم" required>
                    <input type="password" id="reg-password" placeholder="كلمة المرور" required>
                    <input type="text" id="reg-key" placeholder="مفتاح التفعيل" required>
                    <button type="submit">تسجيل</button>
                </form>
                <div class="toggle" onclick="showLogin()">لديك حساب؟ <span>تسجيل الدخول</span></div>
                <div id="message"></div>
            `;
            document.getElementById('registerForm').onsubmit = (e) => { e.preventDefault(); register(); };
        }
        function showLogin() { location.reload(); }
        document.getElementById('loginForm').onsubmit = (e) => { e.preventDefault(); login(); };
    </script>
</body>
</html>'''

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        init_files()
        
        if self.path == '/' or self.path == '/index.py':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_LOGIN.encode())
            return
        
        self.send_response(404)
        self.end_headers()
    
    def do_POST(self):
        init_files()
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        
        parsed = urllib.parse.urlparse(self.path)
        action = urllib.parse.parse_qs(parsed.query).get('action', [''])[0]
        
        if action == 'login':
            username = post_data.get('username')
            password = hash_password(post_data.get('password'))
            
            with open(USERS_FILE, 'r') as f:
                users = json.load(f)
            
            if username in users and users[username]['password'] == password:
                token = str(uuid.uuid4())
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True, 'token': token, 'role': users[username]['role']}).encode())
            else:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': 'بيانات دخول خاطئة'}).encode())
        
        elif action == 'register':
            username = post_data.get('username')
            password = post_data.get('password')
            key = post_data.get('key')
            
            with open(USERS_FILE, 'r') as f:
                users = json.load(f)
            
            with open(KEYS_FILE, 'r') as f:
                keys = json.load(f)
            
            if username in users:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': 'اسم المستخدم موجود'}).encode())
                return
            
            if key not in keys:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': 'مفتاح غير صالح'}).encode())
                return
            
            expiry = datetime.fromisoformat(keys[key]['expiry'])
            if expiry < datetime.now():
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': 'المفتاح منتهي الصلاحية'}).encode())
                return
            
            users[username] = {
                'password': hash_password(password),
                'role': 'user',
                'created': str(datetime.now()),
                'key_used': key,
                'expiry': str(expiry)
            }
            
            with open(USERS_FILE, 'w') as f:
                json.dump(users, f)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True}).encode())
