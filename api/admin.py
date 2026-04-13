import json
import os
from datetime import datetime, timedelta
import hashlib
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

init_files()

HTML_ADMIN = '''<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة المالك - RAGNAR</title>
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
        .logout { background: rgba(255,0,0,0.3); padding: 8px 20px; border-radius: 10px; cursor: pointer; }
        .container { max-width: 1400px; margin: 40px auto; padding: 0 20px; }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: rgba(0,0,0,0.7);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            border: 1px solid rgba(255,102,0,0.3);
        }
        .stat-number { font-size: 48px; font-weight: bold; color: #ff6600; }
        .stat-label { color: #9b59b6; margin-top: 10px; }
        .card {
            background: rgba(0,0,0,0.7);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            border: 1px solid rgba(255,102,0,0.3);
        }
        .card-title {
            font-size: 20px;
            color: #ff6600;
            margin-bottom: 20px;
            border-right: 3px solid #ff6600;
            padding-right: 15px;
        }
        .input-group {
            display: inline-block;
            margin-left: 10px;
        }
        .input-group input, .input-group select {
            padding: 10px 15px;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 8px;
            color: white;
        }
        button {
            background: linear-gradient(90deg, #ff6600, #9b59b6);
            padding: 10px 25px;
            border: none;
            border-radius: 8px;
            color: white;
            cursor: pointer;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 12px;
            text-align: right;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        th { color: #ff6600; }
        .delete-btn { background: rgba(255,0,0,0.5); padding: 5px 15px; font-size: 12px; }
        .delete-btn:hover { background: red; }
        .success { background: rgba(0,255,0,0.2); border: 1px solid green; padding: 10px; border-radius: 8px; margin-top: 10px; color: #00ff00; }
        .error { background: rgba(255,0,0,0.2); border: 1px solid red; padding: 10px; border-radius: 8px; margin-top: 10px; color: #ff4444; }
        code { background: #1a1a1a; padding: 5px 10px; border-radius: 5px; font-family: monospace; }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">RAGNAR <span>CONTROL</span></div>
        <div class="logout" onclick="logout()">تسجيل خروج</div>
    </div>
    <div class="container">
        <div class="stats-grid" id="stats">جاري التحميل...</div>
        
        <div class="card">
            <div class="card-title">🔑 إنشاء مفتاح جديد</div>
            <div class="input-group">
                <input type="text" id="keyName" placeholder="اسم المفتاح" dir="ltr">
            </div>
            <div class="input-group">
                <input type="number" id="days" placeholder="عدد الأيام" value="30">
            </div>
            <button onclick="createKey()">إنشاء مفتاح</button>
            <div id="keyResult"></div>
        </div>
        
        <div class="card">
            <div class="card-title">📊 قائمة المستخدمين</div>
            <div style="overflow-x: auto;">
                <table id="usersTable">
                    <thead>
                        <tr><th>اسم المستخدم</th><th>تاريخ الإنشاء</th><th>صلاحية حتى</th><th>المفتاح المستخدم</th><th>إجراء</th></tr>
                    </thead>
                    <tbody></tbody>
                </table>
            </div>
        </div>
        
        <div class="card">
            <div class="card-title">🔑 المفاتيح النشطة</div>
            <div style="overflow-x: auto;">
                <table id="keysTable">
                    <thead>
                        <tr><th>المفتاح</th><th>صالح حتى</th><th>الأيام المتبقية</th><th>إجراء</th></tr>
                    </thead>
                    <tbody></tbody>
                </table>
            </div>
        </div>
    </div>
    
    <script>
        async function loadData() {
            try {
                const response = await fetch('/api/admin.py?action=get_stats');
                const data = await response.json();
                
                document.getElementById('stats').innerHTML = `
                    <div class="stat-card"><div class="stat-number">${data.total_users || 0}</div><div class="stat-label">إجمالي المستخدمين</div></div>
                    <div class="stat-card"><div class="stat-number">${data.active_keys || 0}</div><div class="stat-label">المفاتيح النشطة</div></div>
                    <div class="stat-card"><div class="stat-number">${data.total_bots || 0}</div><div class="stat-label">البوتات المشغلة</div></div>
                `;
                
                let usersHtml = '';
                if (data.users && data.users.length > 0) {
                    for (const user of data.users) {
                        usersHtml += `<tr>
                            <td>${user.username}</td>
                            <td>${user.created || '-'}</td>
                            <td>${user.expiry || '-'}</td>
                            <td>${user.key_used || '-'}</td>
                            <td><button class="delete-btn" onclick="deleteUser('${user.username}')">حذف</button></td>
                        </tr>`;
                    }
                } else {
                    usersHtml = '<tr><td colspan="5" style="text-align:center">لا يوجد مستخدمين</td></tr>';
                }
                document.querySelector('#usersTable tbody').innerHTML = usersHtml;
                
                let keysHtml = '';
                if (data.keys && data.keys.length > 0) {
                    for (const key of data.keys) {
                        keysHtml += `<tr>
                            <td><code>${key.key}</code></td>
                            <td>${key.expiry}</td>
                            <td>${key.days_left}</td>
                            <td><button class="delete-btn" onclick="deleteKey('${key.key}')">حذف</button></td>
                        </tr>`;
                    }
                } else {
                    keysHtml = '<tr><td colspan="4" style="text-align:center">لا يوجد مفاتيح</td></tr>';
                }
                document.querySelector('#keysTable tbody').innerHTML = keysHtml;
            } catch(e) {
                console.error(e);
                document.getElementById('stats').innerHTML = '<div class="error">خطأ في تحميل البيانات</div>';
            }
        }
        
        async function createKey() {
            const keyName = document.getElementById('keyName').value;
            const days = document.getElementById('days').value;
            
            if (!keyName) {
                document.getElementById('keyResult').innerHTML = '<div class="error">❌ الرجاء إدخال اسم المفتاح</div>';
                return;
            }
            
            document.getElementById('keyResult').innerHTML = '<div class="success">⏳ جاري الإنشاء...</div>';
            
            try {
                const response = await fetch('/api/admin.py?action=create_key', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({key_name: keyName, days: parseInt(days)})
                });
                
                const data = await response.json();
                if (data.success) {
                    document.getElementById('keyResult').innerHTML = '<div class="success">✅ المفتاح: <code>' + data.key + '</code><br>📅 صالح لمدة ' + days + ' يوم</div>';
                    document.getElementById('keyName').value = '';
                    loadData();
                } else {
                    document.getElementById('keyResult').innerHTML = '<div class="error">❌ ' + data.error + '</div>';
                }
            } catch(e) {
                document.getElementById('keyResult').innerHTML = '<div class="error">❌ خطأ في الاتصال بالخادم</div>';
            }
        }
        
        async function deleteUser(username) {
            if (confirm('هل أنت متأكد من حذف المستخدم ' + username + '؟')) {
                const response = await fetch('/api/admin.py?action=delete_user', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username})
                });
                const data = await response.json();
                if (data.success) loadData();
            }
        }
        
        async function deleteKey(key) {
            if (confirm('هل أنت متأكد من حذف المفتاح؟')) {
                const response = await fetch('/api/admin.py?action=delete_key', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({key})
                });
                const data = await response.json();
                if (data.success) loadData();
            }
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
        init_files()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(HTML_ADMIN.encode())
    
    def do_POST(self):
        init_files()
        
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': False, 'error': 'No data received'}).encode())
            return
        
        post_data = json.loads(self.rfile.read(content_length))
        
        parsed = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed.query)
        action = query_params.get('action', [''])[0]
        
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
        
        with open(KEYS_FILE, 'r') as f:
            keys = json.load(f)
        
        with open(TOKEN_FILE, 'r') as f:
            tokens = json.load(f)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if action == 'get_stats':
            active_keys = sum(1 for k, v in keys.items() if datetime.fromisoformat(v['expiry']) > datetime.now())
            
            users_list = []
            for username, data in users.items():
                if username != 'RAGNAR':
                    users_list.append({
                        'username': username,
                        'created': data.get('created', ''),
                        'expiry': data.get('expiry', ''),
                        'key_used': data.get('key_used', '')
                    })
            
            keys_list = []
            for key, data in keys.items():
                expiry = datetime.fromisoformat(data['expiry'])
                days_left = max(0, (expiry - datetime.now()).days)
                keys_list.append({
                    'key': key,
                    'expiry': data['expiry'],
                    'days_left': days_left
                })
            
            self.wfile.write(json.dumps({
                'total_users': len(users_list),
                'active_keys': active_keys,
                'total_bots': len(tokens),
                'users': users_list,
                'keys': keys_list
            }).encode())
        
        elif action == 'create_key':
            key_name = post_data.get('key_name', '').strip()
            days = post_data.get('days', 30)
            
            if not key_name:
                key_name = f"KEY_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            if key_name in keys:
                self.wfile.write(json.dumps({'success': False, 'error': 'المفتاح موجود مسبقاً'}).encode())
                return
            
            expiry = datetime.now() + timedelta(days=days)
            keys[key_name] = {'expiry': expiry.isoformat()}
            
            with open(KEYS_FILE, 'w') as f:
                json.dump(keys, f)
            
            self.wfile.write(json.dumps({'success': True, 'key': key_name}).encode())
        
        elif action == 'delete_user':
            username = post_data.get('username')
            if username in users and username != 'RAGNAR':
                del users[username]
                with open(USERS_FILE, 'w') as f:
                    json.dump(users, f)
                self.wfile.write(json.dumps({'success': True}).encode())
            else:
                self.wfile.write(json.dumps({'success': False, 'error': 'لا يمكن حذف المالك'}).encode())
        
        elif action == 'delete_key':
            key = post_data.get('key')
            if key in keys:
                del keys[key]
                with open(KEYS_FILE, 'w') as f:
                    json.dump(keys, f)
                self.wfile.write(json.dumps({'success': True}).encode())
            else:
                self.wfile.write(json.dumps({'success': False, 'error': 'المفتاح غير موجود'}).encode())
        
        else:
            self.wfile.write(json.dumps({'error': 'Action not found'}).encode())
