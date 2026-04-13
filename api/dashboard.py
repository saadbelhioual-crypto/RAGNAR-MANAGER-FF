import json
import os
from datetime import datetime
from http.server import BaseHTTPRequestHandler
import urllib.parse

DATA_PATH = '/tmp/data/'
TOKEN_FILE = DATA_PATH + 'amine_token.txt'
USERS_FILE = DATA_PATH + 'users.json'

os.makedirs(DATA_PATH, exist_ok=True)

HTML_DASHBOARD = '''<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة التحكم - TCP BOT</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a0033 50%, #000000 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: white;
            min-height: 100vh;
        }
        .header {
            background: rgba(0,0,0,0.9);
            padding: 20px;
            border-bottom: 2px solid #ff6600;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo { font-size: 24px; color: #ff6600; font-weight: bold; }
        .logo span { color: #9b59b6; }
        .logout { background: rgba(255,0,0,0.3); padding: 8px 20px; border-radius: 10px; cursor: pointer; transition: 0.3s; }
        .logout:hover { background: rgba(255,0,0,0.6); }
        .container { max-width: 1200px; margin: 40px auto; padding: 0 20px; }
        .info-card {
            background: rgba(0,0,0,0.7);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            border: 1px solid rgba(255,102,0,0.3);
        }
        .info-title { font-size: 20px; color: #ff6600; margin-bottom: 20px; border-right: 3px solid #ff6600; padding-right: 15px; }
        .days-left {
            background: linear-gradient(90deg, #9b59b6, #ff6600);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-size: 18px;
            margin-bottom: 20px;
        }
        .days-left span { font-size: 28px; font-weight: bold; }
        .input-group { margin-bottom: 20px; }
        .input-group label { display: block; margin-bottom: 8px; color: #9b59b6; }
        .input-group input {
            width: 100%; padding: 12px 15px;
            background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2);
            border-radius: 10px; color: white; font-size: 16px;
        }
        .input-group input:focus { outline: none; border-color: #ff6600; }
        button {
            background: linear-gradient(90deg, #ff6600, #9b59b6);
            padding: 12px 30px; border: none; border-radius: 10px;
            color: white; font-size: 16px; cursor: pointer; font-weight: bold;
        }
        button:hover { transform: scale(1.02); }
        .status {
            margin-top: 20px; padding: 15px; border-radius: 10px;
            text-align: center; font-weight: bold;
        }
        .status-success { background: rgba(0,255,0,0.2); border: 1px solid green; color: #00ff00; }
        .status-error { background: rgba(255,0,0,0.2); border: 1px solid red; color: #ff4444; }
        .saved-list {
            margin-top: 30px;
            background: rgba(0,0,0,0.5);
            border-radius: 10px;
            padding: 15px;
        }
        .saved-item {
            background: rgba(255,102,0,0.1);
            padding: 12px;
            margin: 10px 0;
            border-radius: 8px;
            border-left: 3px solid #ff6600;
        }
        .saved-id { color: #ff6600; font-weight: bold; }
        .saved-token { color: #9b59b6; font-size: 12px; word-break: break-all; }
        .run-btn {
            background: #00aa00;
            margin-top: 10px;
            padding: 8px 20px;
            font-size: 14px;
        }
        .run-btn:hover { background: #00cc00; }
        .delete-btn {
            background: #aa0000;
            margin-top: 10px;
            margin-left: 10px;
            padding: 8px 20px;
            font-size: 14px;
        }
        .delete-btn:hover { background: #cc0000; }
        h3 { color: #ff6600; margin: 20px 0 10px 0; }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">TCP BOT <span>SYSTEM</span></div>
        <div class="logout" onclick="logout()">تسجيل خروج</div>
    </div>
    <div class="container">
        <div class="info-card">
            <div class="info-title">معلومات حسابك</div>
            <div class="days-left" id="daysLeft">جاري التحميل...</div>
            <div class="input-group">
                <label>🎮 الأيدي (UID)</label>
                <input type="text" id="uid" placeholder="أدخل الأيدي الخاص بالحساب">
            </div>
            <div class="input-group">
                <label>🔑 التوكن (Token)</label>
                <input type="text" id="token" placeholder="أدخل التوكن الخاص بالحساب">
            </div>
            <button onclick="saveCredentials()">💾 حفظ البيانات</button>
            <div id="status"></div>
        </div>
        
        <div class="info-card">
            <div class="info-title">الحسابات المحفوظة</div>
            <div id="savedList"></div>
        </div>
    </div>
    
    <script>
        const username = localStorage.getItem('username');
        
        async function loadData() {
            const response = await fetch('/api/dashboard.py?action=get_user_data&username=' + username);
            const data = await response.json();
            
            if (data.days_left !== undefined) {
                document.getElementById('daysLeft').innerHTML = '✅ متبقي في اشتراكك: <span>' + data.days_left + '</span> يوم';
            }
            
            if (data.saved_credentials) {
                let html = '';
                for (const [uid, token] of Object.entries(data.saved_credentials)) {
                    html += `
                        <div class="saved-item">
                            <div class="saved-id">🆔 الأيدي: ${uid}</div>
                            <div class="saved-token">🔐 التوكن: ${token.substring(0, 30)}...</div>
                            <button class="run-btn" onclick="runBot('${uid}', '${token.replace(/'/g, "\\'")}')">▶️ تشغيل البوت</button>
                            <button class="delete-btn" onclick="deleteAccount('${uid}')">🗑️ حذف</button>
                        </div>
                    `;
                }
                document.getElementById('savedList').innerHTML = html || '<p>لا توجد حسابات محفوظة</p>';
            }
        }
        
        async function saveCredentials() {
            const uid = document.getElementById('uid').value;
            const token = document.getElementById('token').value;
            
            if (!uid || !token) {
                showStatus('الرجاء إدخال الأيدي والتوكن', false);
                return;
            }
            
            const response = await fetch('/api/dashboard.py?action=save_credentials', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username, uid, token})
            });
            
            const data = await response.json();
            if (data.success) {
                showStatus('تم حفظ البيانات بنجاح!', true);
                document.getElementById('uid').value = '';
                document.getElementById('token').value = '';
                loadData();
            } else {
                showStatus(data.error, false);
            }
        }
        
        async function runBot(uid, token) {
            showStatus('جاري تشغيل البوت...', true);
            const response = await fetch('/api/dashboard.py?action=run_bot', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username, uid, token})
            });
            const data = await response.json();
            showStatus(data.message, data.success);
        }
        
        async function deleteAccount(uid) {
            if (!confirm('هل أنت متأكد من حذف هذا الحساب؟')) return;
            
            const response = await fetch('/api/dashboard.py?action=delete_account', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username, uid})
            });
            const data = await response.json();
            if (data.success) {
                showStatus('تم حذف الحساب بنجاح', true);
                loadData();
            } else {
                showStatus(data.error, false);
            }
        }
        
        function showStatus(msg, isSuccess) {
            const statusDiv = document.getElementById('status');
            statusDiv.innerHTML = '<div class="status ' + (isSuccess ? 'status-success' : 'status-error') + '">' + msg + '</div>';
            setTimeout(() => { statusDiv.innerHTML = ''; }, 5000);
        }
        
        function logout() {
            localStorage.clear();
            window.location.href = '/';
        }
        
        loadData();
    </script>
</body>
</html>'''

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML_DASHBOARD.encode())
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        
        parsed = urllib.parse.urlparse(self.path)
        action = urllib.parse.parse_qs(parsed.query).get('action', [''])[0]
        
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
        
        # قراءة ملف التوكنات
        current_tokens = {}
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'r') as f:
                try:
                    current_tokens = json.load(f)
                except:
                    current_tokens = {}
        
        if action == 'get_user_data':
            username = post_data.get('username')
            if username in users:
                expiry = datetime.fromisoformat(users[username]['expiry'])
                days_left = max(0, (expiry - datetime.now()).days)
                
                # جلب حسابات هذا المستخدم فقط
                saved_creds = {}
                if username == 'RAGNAR':
                    saved_creds = current_tokens
                else:
                    for uid, token in current_tokens.items():
                        saved_creds[uid] = token
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'days_left': days_left, 'saved_credentials': saved_creds}).encode())
        
        elif action == 'save_credentials':
            username = post_data.get('username')
            uid = post_data.get('uid')
            token = post_data.get('token')
            
            if username not in users:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': 'مستخدم غير موجود'}).encode())
                return
            
            expiry = datetime.fromisoformat(users[username]['expiry'])
            if expiry < datetime.now():
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': 'اشتراكك منتهي'}).encode())
                return
            
            # حفظ التوكن بصيغة {"الأيدي": "التوكن"}
            current_tokens[uid] = token
            
            with open(TOKEN_FILE, 'w') as f:
                json.dump(current_tokens, f, indent=4)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True}).encode())
        
        elif action == 'run_bot':
            username = post_data.get('username')
            uid = post_data.get('uid')
            token = post_data.get('token')
            
            if username not in users:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'message': 'مستخدم غير موجود'}).encode())
                return
            
            expiry = datetime.fromisoformat(users[username]['expiry'])
            if expiry < datetime.now():
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'message': 'اشتراكك منتهي'}).encode())
                return
            
            # حفظ التوكن في الملف بنفس صيغة سورسك
            current_tokens[uid] = token
            
            with open(TOKEN_FILE, 'w') as f:
                json.dump(current_tokens, f, indent=4)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True, 'message': f'✅ تم تشغيل البوت على الأيدي {uid}\n📁 تم حفظ التوكن في amine_token.txt'}).encode())
        
        elif action == 'delete_account':
            username = post_data.get('username')
            uid = post_data.get('uid')
            
            if uid in current_tokens:
                del current_tokens[uid]
                with open(TOKEN_FILE, 'w') as f:
                    json.dump(current_tokens, f, indent=4)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True}).encode())
            else:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': 'الحساب غير موجود'}).encode())
