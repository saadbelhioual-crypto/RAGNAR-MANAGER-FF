import threading
import jwt
import random
from threading import Thread
import json
import requests
import google.protobuf
from protobuf_decoder.protobuf_decoder import Parser
import json

import datetime
from datetime import datetime
from google.protobuf.json_format import MessageToJson
import my_message_pb2
import data_pb2
import base64
import logging
import re
import socket
from google.protobuf.timestamp_pb2 import Timestamp
import jwt_generator_pb2
import os
import binascii
import sys
import psutil
import MajorLoginRes_pb2
from time import sleep
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import time
import urllib3
from important_zitado import*
from byte import*

# --- START: Added for improved error handling and logging ---
# Configure logging to provide clear information about the bot's status and errors.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot_activity.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
# --- END: Added for improved error handling and logging ---


tempid = None
sent_inv = False
start_par = False
pleaseaccept = False
nameinv = "none"
idinv = 0
senthi = False
statusinfo = False
tempdata1 = None
tempdata = None
leaveee = False
leaveee1 = False
data22 = None
isroom = False
isroom2 = False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def encrypt_packet(plain_text, key, iv):
    plain_text = bytes.fromhex(plain_text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return cipher_text.hex()
    
def gethashteam(hexxx):
    a = zitado_get_proto(hexxx)
    if not a:
        raise ValueError("Invalid hex format or empty response from zitado_get_proto")
    data = json.loads(a)
    return data['5']['7']
def getownteam(hexxx):
    a = zitado_get_proto(hexxx)
    if not a:
        raise ValueError("Invalid hex format or empty response from zitado_get_proto")
    data = json.loads(a)
    return data['5']['1']

def get_player_status(packet):
    json_result = get_available_room(packet)
    parsed_data = json.loads(json_result)

    if "5" not in parsed_data or "data" not in parsed_data["5"]:
        return "OFFLINE"

    json_data = parsed_data["5"]["data"]

    if "1" not in json_data or "data" not in json_data["1"]:
        return "OFFLINE"

    data = json_data["1"]["data"]

    if "3" not in data:
        return "OFFLINE"

    status_data = data["3"]

    if "data" not in status_data:
        return "OFFLINE"

    status = status_data["data"]

    if status == 1:
        return "SOLO"
    
    if status == 2:
        if "9" in data and "data" in data["9"]:
            group_count = data["9"]["data"]
            countmax1 = data["10"]["data"]
            countmax = countmax1 + 1
            return f"INSQUAD ({group_count}/{countmax})"

        return "INSQUAD"
    
    if status in [3, 5]:
        return "INGAME"
    if status == 4:
        return "IN ROOM"
    
    if status in [6, 7]:
        return "IN SOCIAL ISLAND MODE .."

    return "NOTFOUND"
def get_idroom_by_idplayer(packet):
    json_result = get_available_room(packet)
    parsed_data = json.loads(json_result)
    json_data = parsed_data["5"]["data"]
    data = json_data["1"]["data"]
    idroom = data['15']["data"]
    return idroom
def get_leader(packet):
    json_result = get_available_room(packet)
    parsed_data = json.loads(json_result)
    json_data = parsed_data["5"]["data"]
    data = json_data["1"]["data"]
    leader = data['8']["data"]
    return leader
def generate_random_color():
	color_list = [
    "[00FF00][b][c]",
    "[FFDD00][b][c]",
    "[3813F3][b][c]",
    "[FF0000][b][c]",
    "[0000FF][b][c]",
    "[FFA500][b][c]",
    "[DF07F8][b][c]",
    "[11EAFD][b][c]",
    "[DCE775][b][c]",
    "[A8E6CF][b][c]",
    "[7CB342][b][c]",
    "[FF0000][b][c]",
    "[FFB300][b][c]",
    "[90EE90][b][c]"
]
	random_color = random.choice(color_list)
	return  random_color

def fix_num(num):
    fixed = ""
    count = 0
    num_str = str(num)  # Convert the number to a string

    for char in num_str:
        if char.isdigit():
            count += 1
        fixed += char
        if count == 3:
            fixed += "[c]"
            count = 0  
    return fixed


def fix_word(num):
    fixed = ""
    count = 0
    
    for char in num:
        if char:
            count += 1
        fixed += char
        if count == 3:
            fixed += "[c]"
            count = 0  
    return fixed
    
def check_banned_status(player_id):
   
    url = f"http://amin-team-api.vercel.app/check_banned?player_id={player_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data  
        else:
            return {"error": f"Failed to fetch data. Status code: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}
        

# --- START: REVISED FUNCTION TO FIX THE "INVALID ID" ERROR ---
def send_vistttt(uid):
    try:
        # Step 1: Directly call the new visit API, removing the faulty dependency on newinfo.
        api_url = f"https://visit.vercel.app/ind/{uid}"
        response = requests.get(api_url, timeout=15)

        # Step 2: Process the API response.
        if response.status_code == 200:
            data = response.json()
            success_count = data.get('success', 0)

            # The primary check is now the 'success' count from the visit API itself.
            if success_count > 0:
                # Extract all details from the successful response.
                nickname = data.get('nickname', 'N/A')
                level = data.get('level', 'N/A')
                likes = data.get('likes', 0)
                
                # Format a premium success message.
                return (
                    f"[b][c][00FF00]╔═ ✅ Visit Success ✅ ═╗\n\n"
                    f"[FFFFFF]Successfully sent [FFFF00]{success_count}[FFFFFF] visits to:\n\n"
                    f"[00BFFF]👤 Nickname: [FFFFFF]{nickname}\n"
                    f"[00BFFF]🆔 Player ID: [FFFFFF]{fix_num(uid)}\n"
                    f"[00BFFF]🎖️ Level: [FFFFFF]{level}\n"
                    f"[00BFFF]❤️ Likes: [FFFFFF]{fix_num(likes)}\n\n"
                    f"[00FF00]╚══════════╝"
                )
            else:
                # This handles cases where the API returns 200 but sends 0 visits,
                # which could mean the daily limit is reached or the ID is invalid.
                return (
                    f"[b][c][FF0000]╔═「 ❌ Failed ❌ 」═╗\n\n"
                    f"[FFFFFF]Could not send visits to ID: [FFFF00]{fix_num(uid)}\n"
                    f"[FFFFFF]The ID may be invalid or the daily\n"
                    f"[FFFFFF]visit limit has been reached.\n\n"
                    f"[FF0000]╚══════════╝"
                )
        else:
            # Handle API server errors (like 402, 404, 500). This now serves
            # as the primary "Invalid ID" check.
            return (
                f"[b][c][FF0000]╔═「 ❌ Error ❌ 」═╗\n\n"
                f"[FFFFFF]Invalid Player ID or API Error.\n"
                f"[FFFFFF]Server returned status: [FFFF00]{response.status_code}\n\n"
                f"[FF0000]╚══════════╝"
            )

    except requests.exceptions.RequestException:
        # Handle network or connection errors.
        return (
            f"[b][c][FF0000]╔═「 🔌 Connection Error 🔌 」═╗\n\n"
            f"[FFFFFF]Could not connect to the visit API server.\n"
            f"[FFFFFF]Please try again later.\n\n"
            f"[FF0000]╚══════════╝"
        )
    except Exception as e:
        # Handle any other unexpected errors.
        logging.error(f"An unexpected error occurred in send_vistttt: {str(e)}")
        return (
            f"[b][c][FF0000]╔═「 ⚙️ System Error ⚙️ 」═╗\n\n"
            f"[FFFFFF]An unexpected error occurred.\n"
            f"[FFFFFF]Check the logs for more details.\n\n"
            f"[FF0000]╚══════════╝"
        )
# --- END: REVISED FUNCTION ---


def rrrrrrrrrrrrrr(number):
    if isinstance(number, str) and '***' in number:
        return number.replace('***', '106')
    return number
def newinfo(uid):
    try:
        # The new API URL
        url = f"https://jnl-tcp-info.vercel.app/player-info?uid={uid}"
        # Make the request with a timeout to prevent it from hanging
        response = requests.get(url, timeout=15)

        # A successful request returns status code 200
        if response.status_code == 200:
            data = response.json()
            # Check for a key like 'AccountName' to confirm the API returned valid data
            if "AccountName" in data and data["AccountName"]:
                return {"status": "ok", "info": data}
            else:
                # This handles cases where the API returns 200 but the ID was invalid
                return {"status": "wrong_id"}
        else:
            logging.error(f"Error: API returned status code {response.status_code} for UID {uid}")
            return {"status": "wrong_id"}

    except requests.exceptions.RequestException as e:
        # Handle network issues like timeouts or connection errors
        logging.error(f"Error during newinfo request: {str(e)}")
        return {"status": "error", "message": str(e)}
    except Exception as e:
        # Handle any other unexpected errors
        logging.error(f"An unexpected error occurred in newinfo: {str(e)}")
        return {"status": "error", "message": str(e)}
	
import requests

# --- START: CORRECTED SPAM FUNCTION TO FIX "ERROR IN ID" ---
def send_spam(uid):
    try:
        # Step 1: Directly call the new spam API. The faulty newinfo() check has been removed.
        api_url = f"https://spam.vercel.app/send_requests?uid={uid}"
        response = requests.get(api_url, timeout=15)

        # Step 2: Process the detailed API response.
        if response.status_code == 200:
            data = response.json()
            success_count = data.get('success_count', 0)
            failed_count = data.get('failed_count', 0)

            # Check if the API managed to send any requests successfully.
            if success_count > 0:
                # Format a detailed success message.
                return (
                    f"[b][c][00FF00]╔═══ ✅ Spam Success ✅ ═══╗\n\n"
                    f"[FFFFFF]Friend requests sent to:\n"
                    f"[00BFFF]🆔 Player ID: [FFFFFF]{fix_num(uid)}\n\n"
                    f"[00FF00]✓ Success: [FFFFFF]{success_count}\n"
                    f"[FF0000]✗ Failed:  [FFFFFF]{failed_count}\n\n"
                    f"[00FF00]╚══════════════════════╝"
                )
            else:
                # Handle cases where the API call worked but no requests were sent.
                # This could mean the ID is invalid or a server limit was hit.
                return (
                    f"[b][c][FF0000]╔═══════「 ⚠️ Failed ⚠️ 」═══════╗\n\n"
                    f"[FFFFFF]Could not send requests to ID:\n"
                    f"[FFFF00]{fix_num(uid)}\n\n"
                    f"[FFFFFF]The ID may be invalid or the\n"
                    f"[FFFFFF]server has reached its limit.\n"
                    f"[FF0000]╚═══════════════════════════╝"
                )
        else:
            # Handle API server errors (e.g., 404, 500).
            return (
                f"[b][c][FF0000]╔═══════「 ❌ API Error ❌ 」═══════╗\n\n"
                f"[FFFFFF]The spam server returned an error.\n"
                f"[FFFFFF]Status Code: [FFFF00]{response.status_code}\n\n"
                f"[FF0000]╚════════════════════════════╝"
            )

    except requests.exceptions.RequestException:
        # Handle network or connection errors.
        return (
            f"[b][c][FF0000]╔════「 🔌 Connection Error 🔌 」════╗\n\n"
            f"[FFFFFF]Could not connect to the spam API server.\n"
            f"[FFFFFF]Please try again later.\n\n"
            f"[FF0000]╚══════════════════════════════╝"
        )
    except Exception as e:
        # Handle any other unexpected errors.
        logging.error(f"An unexpected error occurred in send_spam: {str(e)}")
        return (
            f"[b][c][FF0000]╔════「 ⚙️ System Error ⚙️ 」════╗\n\n"
            f"[FFFFFF]An unexpected error occurred.\n"
            f"[FFFFFF]Check the logs for more details.\n\n"
            f"[FF0000]╚══════════════════════════╝"
        )
# --- END: CORRECTED SPAM FUNCTION ---
def attack_profail(player_id):
    url = f"https://visit-taupe.vercel.app/visit/{player_id}"
    res = requests.get(url)
    if res.status_code() == 200:
        logging.info("Done-Attack")
    else:
        logging.error("Fuck-Attack")

def send_likes(uid):
    try:
        # The new API URL with the provided key
        api_url = f"https://ron.vercel.app/like?uid={uid}&server_name=ind&key=W8IDwCgQbMXYyxNUCmPhcBb3tW56ys3Y"
        
        # Make the request with a timeout to prevent it from hanging
        likes_api_response = requests.get(api_url, timeout=15)
        
        # Check if the API request was successful (HTTP 200 OK)
        if likes_api_response.status_code == 200:
            api_json_response = likes_api_response.json()
            
            # The actual data is inside the "response" object
            response_data = api_json_response.get('response', {})
            
            # Extract all relevant fields from the API response
            likes_added = response_data.get('LikesGivenByAPI', 0)
            player_name = response_data.get('PlayerNickname', 'N/A')
            likes_before = response_data.get('LikesbeforeCommand', 0)
            likes_after = response_data.get('LikesafterCommand', 0)
            key_remaining = response_data.get('KeyRemainingRequests', 'N/A')

            # This is the success case, where LikesGivenByAPI is greater than 0
            if likes_added > 0:
                return {
                    "status": "ok",
                    "message": (
                        f"[C][B][00FF00]________________________\n"
                        f" ✅ Likes Sent Successfully!\n\n"
                        f" 👤 Name: {player_name}\n"
                        f" 🌏 Region: IND\n"
                        f" 👍 Likes Given: [FFFF00]{likes_added}\n"  # This line shows the total likes sent
                        f" ❤️ Before: {likes_before} ➔ After: {likes_after}\n\n"
                        f" 🔑 Key Remaining: [00FFFF]{key_remaining}\n"
                        f"________________________"
                    )
                }
            else:
                # This is the case where the daily limit for that specific UID has been reached
                return {
                    "status": "failed",
                    "message": (
                        f"[C][B][FF0000]________________________\n"
                        f" ❌ Daily like limit reached for this UID.\n"
                        f" Please try again after 4 AM IST or use a different UID.\n\n"
                        f" 🔑 Key Remaining: [00FFFF]{key_remaining}\n"
                        f"________________________"
                    )
                }
        else:
            # This handles API server errors (e.g., 404 Not Found, 500 Internal Server Error)
            return {
                "status": "failed",
                "message": (
                    f"[C][B][FF0000]________________________\n"
                    f" ❌ API Error!\n"
                    f" Status Code: {likes_api_response.status_code}\n"
                    f" Please check the UID and try again.\n"
                    f"________________________"
                )
            }

    except requests.exceptions.RequestException:
        # This handles network errors (e.g., timeout, no connection)
        return {
            "status": "failed",
            "message": (
                f"[C][B][FF0000]________________________\n"
                f" ❌ API Connection Failed!\n"
                f" The like server may be down. Please try again later.\n"
                f"________________________"
            )
        }
    except Exception as e:
        # This catches any other unexpected errors
        return {
            "status": "failed",
            "message": (
                f"[C][B][FF0000]________________________\n"
                f" ❌ An unexpected error occurred: {str(e)}\n"
                f"________________________"
            )
        }

def get_info(uid):
    try:
        # Attempt to connect to the player info API
        info_api_response = requests.get(
            f"https://jnl-tcp-info.vercel.app/player-info?uid={uid}",
            timeout=15  # Add a timeout to prevent it from hanging
        )
        
        # Check if the API request was successful
        if info_api_response.status_code == 200:
            api_json_response = info_api_response.json()
            
            # Extract relevant fields from the response
            account_name = api_json_response.get('AccountName', 'Unknown')
            account_level = api_json_response.get('AccountLevel', 0)
            account_likes = api_json_response.get('AccountLikes', 0)
            account_region = api_json_response.get('AccountRegion', 'Unknown')
            br_max_rank = api_json_response.get('BrMaxRank', 0)
            cs_max_rank = api_json_response.get('CsMaxRank', 0)
            guild_name = api_json_response.get('GuildName', 'None')
            signature = api_json_response.get('signature', 'No signature')

            # Case: Success with player details
            return {
                "status": "ok",
                "message": (
                    f"[C][B][00FF00]________________________\n"
                    f" ✅ Player Information\n"
                    f" Name: {account_name}\n"
                    f" Level: {account_level}\n"
                    f" Likes: {account_likes}\n"
                    f" Region: {account_region}\n"
                    f" BR Max Rank: {br_max_rank}\n"
                    f" CS Max Rank: {cs_max_rank}\n"
                    f" Guild: {guild_name}\n"
                    f" Signature: {signature}\n"
                    f"________________________"
                )
            }
        else:
            # Case: General API failure
            return {
                "status": "failed",
                "message": (
                    f"[C][B][FF0000]________________________\n"
                    f" ❌ Failed to fetch player info!\n"
                    f" Please check the validity of the User ID\n"
                    f"________________________"
                )
            }

    except requests.exceptions.RequestException:
        # Handle network errors (e.g., API is not running)
        return {
            "status": "failed",
            "message": (
                f"[C][B][FF0000]________________________\n"
                f" ❌ API Connection Failed!\n"
                f" Please ensure the API server is running\n"
                f"________________________"
            )
        }
    except Exception as e:
        # Catch any other unexpected errors
        return {
            "status": "failed",
            "message": (
                f"[C][B][FF0000]________________________\n"
                f" ❌ An unexpected error occurred: {str(e)}\n"
                f"________________________"
            )
        }        
		
def Encrypt(number):
    number = int(number)  # Convert the number to an integer
    encoded_bytes = []    # Create a list to store the encoded bytes

    while True:  # Loop that continues until the number is fully encoded
        byte = number & 0x7F  # Extract the least 7 bits of the number
        number >>= 7  # Shift the number to the right by 7 bits
        if number:
            byte |= 0x80  # Set the eighth bit to 1 if the number still contains additional bits

        encoded_bytes.append(byte)
        if not number:
            break  # Stop if no additional bits are left in the number

    return bytes(encoded_bytes).hex()
    


def get_random_avatar():
	avatar_list = [
         '902050001', '902050002', '902050003', '902039016', '902050004', 
        '902047011', '902047010', '902049015', '902050006', '902049020'
    ]
	random_avatar = random.choice(avatar_list)
	return  random_avatar

class FF_CLIENT(threading.Thread):
    def __init__(self, id, password):
        self.id = id
        self.password = password
        self.key = None
        self.iv = None
        self.get_tok()
    def connect(self, tok, host, port, packet, key, iv):
        global clients
        clients = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = int(port)
        clients.connect((host, port))
        clients.send(bytes.fromhex(tok))

        while True:
            data = clients.recv(9999)
            if data == b"":
                logging.error("Connection closed by remote host")
                break
def get_available_room(input_text):
    try:
        parsed_results = Parser().parse(input_text)
        parsed_results_objects = parsed_results
        parsed_results_dict = parse_results(parsed_results_objects)
        json_data = json.dumps(parsed_results_dict)
        return json_data
    except Exception as e:
        logging.error(f"error {e}")
        return None

def parse_results(parsed_results):
    result_dict = {}
    for result in parsed_results:
        field_data = {}
        field_data["wire_type"] = result.wire_type
        if result.wire_type == "varint":
            field_data["data"] = result.data
        if result.wire_type == "string":
            field_data["data"] = result.data
        if result.wire_type == "bytes":
            field_data["data"] = result.data
        elif result.wire_type == "length_delimited":
            field_data["data"] = parse_results(result.data.results)
        result_dict[result.field] = field_data
    return result_dict

def dec_to_hex(ask):
    ask_result = hex(ask)
    final_result = str(ask_result)[2:]
    if len(final_result) == 1:
        final_result = "0" + final_result
    return final_result

def encrypt_message(plaintext):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(plaintext, AES.block_size)
    encrypted_message = cipher.encrypt(padded_message)
    return binascii.hexlify(encrypted_message).decode('utf-8')

def encrypt_api(plain_text):
    plain_text = bytes.fromhex(plain_text)
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return cipher_text.hex()

def extract_jwt_from_hex(hex):
    byte_data = binascii.unhexlify(hex)
    message = jwt_generator_pb2.Garena_420()
    message.ParseFromString(byte_data)
    json_output = MessageToJson(message)
    token_data = json.loads(json_output)
    return token_data
    

def format_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# --- START: Modified for improved error handling ---
# This function is now the single point for safely restarting the script.
def restart_program():
    logging.warning("Initiating bot restart...")
    try:
        p = psutil.Process(os.getpid())
        # Close open file descriptors
        for handler in p.open_files() + p.connections():
            try:
                os.close(handler.fd)
            except Exception as e:
                logging.error(f"Failed to close handler {handler.fd}: {e}")
    except Exception as e:
        logging.error(f"Error during pre-restart cleanup: {e}")
    
    # Replace the current process with a new instance of the script
    python = sys.executable
    os.execl(python, python, *sys.argv)
# --- END: Modified for improved error handling ---
          
class FF_CLIENT(threading.Thread):
    def __init__(self, id, password):
        super().__init__()
        self.id = id
        self.password = password
        self.key = None
        self.iv = None
        # --- START: Added for periodic restart ---
        # Record the start time to track uptime.
        self.start_time = time.time()
        # --- END: Added for periodic restart ---
        self.get_tok()

    def parse_my_message(self, serialized_data):
        try:
            MajorLogRes = MajorLoginRes_pb2.MajorLoginRes()
            MajorLogRes.ParseFromString(serialized_data)
            key = MajorLogRes.ak
            iv = MajorLogRes.aiv
            if isinstance(key, bytes):
                key = key.hex()
            if isinstance(iv, bytes):
                iv = iv.hex()
            self.key = key
            self.iv = iv
            logging.info(f"Key: {self.key} | IV: {self.iv}")
            return self.key, self.iv
        except Exception as e:
            logging.error(f"{e}")
            return None, None

    def nmnmmmmn(self, data):
        key, iv = self.key, self.iv
        try:
            key = key if isinstance(key, bytes) else bytes.fromhex(key)
            iv = iv if isinstance(iv, bytes) else bytes.fromhex(iv)
            data = bytes.fromhex(data)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            cipher_text = cipher.encrypt(pad(data, AES.block_size))
            return cipher_text.hex()
        except Exception as e:
            logging.error(f"Error in nmnmmmmn: {e}")

    
    def send_emote(self, target_id, emote_id):
        """
        Creates and prepares the packet for sending an emote to a target player.
        """
        fields = {
            1: 21,
            2: {
                1: 804266360,  # Constant value from original code
                2: 909000001,  # Constant value from original code
                5: {
                    1: int(target_id),
                    3: int(emote_id),
                }
            }
        }
        packet = create_protobuf_packet(fields).hex()
        # The packet type '0515' is used for online/squad actions
        header_lenth = len(encrypt_packet(packet, self.key, self.iv)) // 2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "051500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "05150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0515000" + header_lenth_final + self.nmnmmmmn(packet)
        else:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)    

    
    def spam_room(self, idroom, idplayer):
        fields = {
        1: 78,
        2: {
            1: int(idroom),
            2: "iG:[C][B][FF0000] @BANECIPHERXR",
            4: 330,
            5: 6000,
            6: 201,
            10: int(get_random_avatar()),
            11: int(idplayer),
            12: 1
        }
        }
        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, key, iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0E15000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "0E1500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "0E150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0E15000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)
    def send_squad(self, idplayer):
        fields = {
            1: 33,
            2: {
                1: int(idplayer),
                2: "IND",
                3: 1,
                4: 1,
                7: 330,
                8: 19459,
                9: 100,
                12: 1,
                16: 1,
                17: {
                2: 94,
                6: 11,
                8: "1.109.5",
                9: 3,
                10: 2
                },
                18: 201,
                23: {
                2: 1,
                3: 1
                },
                24: int(get_random_avatar()),
                26: {},
                28: {}
            }
        }
        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, key, iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "051500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "05150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0515000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)
    def start_autooo(self):
        fields = {
        1: 9,
        2: {
            1: 12480598706
        }
        }
        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, key, iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "051500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "05150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0515000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)
    def invite_skwad(self, idplayer):
        fields = {
        1: 2,
        2: {
            1: int(idplayer),
            2: "IND",
            4: 1
        }
        }
        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, key, iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "051500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "05150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0515000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)
    def request_join_squad(self, idplayer):
        fields = {
        1: 33,
        2: {
            1: int(idplayer),
            2: "IND",
            3: 1,
            4: 1,
            5: bytes([1, 7, 9, 10, 11, 18, 25, 26, 32]),
            6: "iG:[C][B][FF0000] @BANECIPHERXR",
            7: 330,
            8: 1000,
            10: "IND",
            11: bytes([49, 97, 99, 52, 98, 56, 48, 101, 99, 102, 48, 52, 55, 56,
            97, 52, 52, 50, 48, 51, 98, 102, 56, 102, 97, 99, 54, 49, 50, 48, 102, 53]),
            12: 1,
            13: int(idplayer),
            14: {
            1: 2203434355,
            2: 8,
            3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
            },
            16: 1,
            17: 1,
            18: 312,
            19: 46,
            23: bytes([16, 1, 24, 1]),
            24: int(get_random_avatar()),
            26: "",
            28: "",
            31: {
            1: 1,
            2: 4096
            },
            32: 4096
        },
        10: "en",
        13: {
            2: 1,
            3: 1
        }
        }
        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, key, iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "051500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "05150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0515000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)
    def request_join_fffffsquad(self, idplayer):
        fields = {
        1: 33,
        2: {
            1: int(idplayer),
            2: "IND",
            3: 1,
            4: 1,
            7: 330,
            8: 19459,
            9: 100,
            12: 1,
            16: 1,
            17: {
            2: 94,
            6: 11,
            8: "1.109.5",
            9: 3,
            10: 2
            },
            18: 201,
            23: {
            2: 1,
            3: 1
            },
            24: int(get_random_avatar()),
            26: {},
            28: {}
        }
        }
        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, key, iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "051500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "05150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0515000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)
    def skwad_maker(self):
        fields = {
        1: 1,
        2: {
            2: "\u0001",
            3: 1,
            4: 1,
            5: "en",
            9: 1,
            11: 1,
            13: 1,
            14: {
            2: 5756,
            6: 11,
            8: "1.109.5",
            9: 3,
            10: 2
            },
        }
        }

        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, key, iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "051500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "05150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0515000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)
    def changes(self, num):
        fields = {
        1: 17,
        2: {
            1: 12480598706,
            2: 1,
            3: int(num),
            4: 60,
            5: "\u001a",
            8: 5,
            13: 329
        }
        }

        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, key, iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "051500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "05150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0515000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)
   
    def leave_s(self):
        fields = {
        1: 7,
        2: {
            1: 12480598706
        }
        }

        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, key, iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "051500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "05150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0515000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)
    def leave_room(self, idroom):
        fields = {
        1: 6,
        2: {
            1: int(idroom)
        }
        }

        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, key, iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0E15000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "0E1500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "0E150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0E15000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)
    def stauts_infoo(self, idd):
        fields = {
        1: 7,
        2: {
            1: 12480598706
        }
        }

        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, key, iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "051500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "05150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0515000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)
        #logging.info(Besto_Packet)
    def GenResponsMsg(self, Msg, Enc_Id):
        fields = {
            1: 1,
            2: {
                1: 12947146032,
                2: Enc_Id,
                3: 2,
                4: str(Msg),
                5: int(datetime.now().timestamp()),
                7: 2,
                9: {
                    1: "BANECIPHERXR",
                    2: int(get_random_avatar()),
                    3: 901049014,
                    4: 330,
                    5: 801040108,
                    8: "Friend",
                    10: 1,
                    11: 1,
                    13: {
                        1: 2,
                        2: 1,
                    },
                    14: {
                        1: 11017917409,
                        2: 8,
                        3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
                    }
                },
                10: "IND",
                13: {
                    1: "https://graph.facebook.com/v9.0/253082355523299/picture?width=160&height=160",
                    2: 1,
                    3: 1
                },
                14: {
                    1: {
                        1: random.choice([1, 4]),
                        2: 1,
                        3: random.randint(1, 180),
                        4: 1,
                        5: int(datetime.now().timestamp()),
                        6: "IND"
                    }
                }
            }
        }

        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, key, iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "1215000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "121500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "12150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "1215000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)
    def createpacketinfo(self, idddd):
        ida = Encrypt(idddd)
        packet = f"080112090A05{ida}1005"
        header_lenth = len(encrypt_packet(packet, key, iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0F15000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "0F1500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "0F150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0F15000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)
    def accept_sq(self, hashteam, idplayer, ownerr):
        fields = {
        1: 4,
        2: {
            1: int(ownerr),
            3: int(idplayer),
            4: "\u0001\u0007\t\n\u0012\u0019\u001a ",
            8: 1,
            9: {
            2: 1393,
            4: "AlwaysJexarHere",
            6: 11,
            8: "1.109.5",
            9: 3,
            10: 2
            },
            10: hashteam,
            12: 1,
            13: "en",
            16: "OR"
        }
        }

        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, key, iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "051500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "05150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0515000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)
    def info_room(self, idrooom):
        fields = {
        1: 1,
        2: {
            1: int(idrooom),
            3: {},
            4: 1,
            6: "en"
        }
        }

        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_lenth = len(encrypt_packet(packet, key, iv))//2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0E15000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "0E1500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "0E150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0E15000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)

    def sockf1(self, tok, online_ip, online_port, packet, key, iv):
        global socket_client
        global sent_inv
        global tempid
        global start_par
        global clients
        global pleaseaccept
        global tempdata1
        global nameinv
        global idinv
        global senthi
        global statusinfo
        global tempdata
        global data22
        global leaveee
        global isroom
        global isroom2
        socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        online_port = int(online_port)

        socket_client.connect((online_ip,online_port))
        logging.info(f" Con port {online_port} Host {online_ip} ")
        #logging.info(tok)
        socket_client.send(bytes.fromhex(tok))
        while True:
            try:
                # --- START: Added for periodic restart ---
                if time.time() - self.start_time > 600: # 10 minutes * 60 seconds
                    logging.warning("Scheduled 10-minute restart from sockf1.")
                    restart_program()
                # --- END: Added for periodic restart ---

                data2 = socket_client.recv(9999)
                #logging.info(data2)
                if "0500" in data2.hex()[0:4]:
                    accept_packet = f'08{data2.hex().split("08", 1)[1]}'
                    kk = get_available_room(accept_packet)
                    parsed_data = json.loads(kk)
                    fark = parsed_data.get("4", {}).get("data", None)
                    if fark is not None:
                        #logging.info(f"haaaaaaaaaaaaaaaaaaaaaaho {fark}")
                        if fark == 18:
                            if sent_inv:
                                accept_packet = f'08{data2.hex().split("08", 1)[1]}'
                                #logging.info(accept_packet)
                                #logging.info(tempid)
                                aa = gethashteam(accept_packet)
                                ownerid = getownteam(accept_packet)
                                #logging.info(ownerid)
                                #logging.info(aa)
                                ss = self.accept_sq(aa, tempid, int(ownerid))
                                socket_client.send(ss)
                                sleep(1)
                                startauto = self.start_autooo()
                                socket_client.send(startauto)
                                start_par = False
                                sent_inv = False
                        if fark == 6:
                            leaveee = True
                            logging.info("kaynaaaaaaaaaaaaaaaa")
                        if fark == 50:
                            pleaseaccept = True
                    #logging.info(data2.hex())

                if "0600" in data2.hex()[0:4] and len(data2.hex()) > 700:
                        accept_packet = f'08{data2.hex().split("08", 1)[1]}'
                        kk = get_available_room(accept_packet)
                        parsed_data = json.loads(kk)
                        #logging.info(parsed_data)
                        idinv = parsed_data["5"]["data"]["1"]["data"]
                        nameinv = parsed_data["5"]["data"]["3"]["data"]
                        senthi = True
                if "0f00" in data2.hex()[0:4]:
                    packett = f'08{data2.hex().split("08", 1)[1]}'
                    #logging.info(packett)
                    kk = get_available_room(packett)
                    parsed_data = json.loads(kk)
                    
                    asdj = parsed_data["2"]["data"]
                    tempdata = get_player_status(packett)
                    if asdj == 15:
                        if tempdata == "OFFLINE":
                            tempdata = f"The id is {tempdata}"
                        else:
                            idplayer = parsed_data["5"]["data"]["1"]["data"]["1"]["data"]
                            idplayer1 = fix_num(idplayer)
                            if tempdata == "IN ROOM":
                                idrooom = get_idroom_by_idplayer(packett)
                                idrooom1 = fix_num(idrooom)
                                
                                tempdata = f"id : {idplayer1}\nstatus : {tempdata}\nid room : {idrooom1}"
                                data22 = packett
                                #logging.info(data22)
                                
                            if "INSQUAD" in tempdata:
                                idleader = get_leader(packett)
                                idleader1 = fix_num(idleader)
                                tempdata = f"id : {idplayer1}\nstatus : {tempdata}\nleader id : {idleader1}"
                            else:
                                tempdata = f"id : {idplayer1}\nstatus : {tempdata}"
                        statusinfo = True 

                        #logging.info(data2.hex())
                        #logging.info(tempdata)
                    
                        

                    else:
                        pass
                if "0e00" in data2.hex()[0:4]:
                    packett = f'08{data2.hex().split("08", 1)[1]}'
                    #logging.info(packett)
                    kk = get_available_room(packett)
                    parsed_data = json.loads(kk)
                    idplayer1 = fix_num(idplayer)
                    asdj = parsed_data["2"]["data"]
                    tempdata1 = get_player_status(packett)
                    if asdj == 14:
                        nameroom = parsed_data["5"]["data"]["1"]["data"]["2"]["data"]
                        
                        maxplayer = parsed_data["5"]["data"]["1"]["data"]["7"]["data"]
                        maxplayer1 = fix_num(maxplayer)
                        nowplayer = parsed_data["5"]["data"]["1"]["data"]["6"]["data"]
                        nowplayer1 = fix_num(nowplayer)
                        tempdata1 = f"{tempdata}\nRoom name : {nameroom}\nMax player : {maxplayer1}\nLive player : {nowplayer1}"
                        #logging.info(tempdata1)
                        

                        
                    
                        
                if data2 == b"":
                    
                    logging.error("Connection closed by remote host in sockf1. Restarting.")
                    restart_program()
                    break
            except Exception as e:
                logging.critical(f"Unhandled error in sockf1 loop: {e}. Restarting bot.")
                restart_program()
    
    
    def connect(self, tok, packet, key, iv, whisper_ip, whisper_port, online_ip, online_port):
        global clients
        global socket_client
        global sent_inv
        global tempid
        global leaveee
        global start_par
        global nameinv
        global idinv
        global senthi
        global statusinfo
        global tempdata
        global pleaseaccept
        global tempdata1
        global data22
        clients = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clients.connect((whisper_ip, whisper_port))
        clients.send(bytes.fromhex(tok))
        thread = threading.Thread(
            target=self.sockf1, args=(tok, online_ip, online_port, "anything", key, iv)
        )
        threads.append(thread)
        thread.start()

        while True:
            # --- START: Added for periodic restart and error handling ---
            if time.time() - self.start_time > 600: # 10 minutes * 60 seconds
                logging.warning("Scheduled 10-minute restart from connect loop.")
                restart_program()
            
            try:
            # --- END: Added for periodic restart and error handling ---
                data = clients.recv(9999)

                if data == b"":
                    logging.error("Connection closed by remote host in connect loop. Restarting.")
                    restart_program()
                    break
                #logging.info(f"Received data: {data}")
                
                if senthi == True:
                    
                    clients.send(
                            self.GenResponsMsg(
                                f"""[C][B][FF1493]╔══════════════════════════╗
[FFFFFF]✨ Hello!  
[FFFFFF]❤️ Thank you for adding me!  
[FFFFFF]⚡ To see my commands:  
[FFFFFF]👉 Send /help or any emoji  
[FF1493]╠══════════════════════════╣
[FFFFFF]🤖 Want to buy a bot?  
[FFFFFF]📩 Contact the developer  
[FFD700]👑 NAME : [FFFF00]BANECIPHERXR
[FFD700]📌 TELEGRAM : [00BFFF]@BANECIPHERXR  
[FF1493]╚══════════════════════════╝""", idinv
                            )
                    )
                    senthi = False
#-------------------------------------------------------------#                
                if "1200" in data.hex()[0:4]:
                
                    json_result = get_available_room(data.hex()[10:])
                    #logging.info(data.hex())
                    parsed_data = json.loads(json_result)
                    try:
                        uid = parsed_data["5"]["data"]["1"]["data"]
                    except KeyError:
                        logging.warning("Warning: '1' key is missing in parsed_data, skipping...")
                        uid = None  # Set a default value
                    if "8" in parsed_data["5"]["data"] and "data" in parsed_data["5"]["data"]["8"]:
                        uexmojiii = parsed_data["5"]["data"]["8"]["data"]
                        if uexmojiii == "DefaultMessageWithKey":
                            pass
                        else:
                            clients.send(
                                self.GenResponsMsg(
                                f"""[FF0000][c]━━━━━━━━━━━━━━━━━━━━[/c]

[FFD700][b][c]✨ Welcome, brother! I am always ready to help you 😊 ✨[/b]

[FFFFFF][c]To find out your commands, send this command:  

[32CD32][b][c]/🤔help[/b]

[FF0000][c]━━━━━━━━━━━━━━━━━━━━[/c]

[FFD700][b][c]For support or to get your personal bot, contact:[/b]

[1E90FF][b][c]Telegram Name: BANECIPHER XR[/b]
[1E90FF][c]@banecipherLIVEE [/c]

[FFD700][b][c]Developer: BANECIPHER XR[/b]

[FF0000][c]━━━━━━━━━━━━━━━━━━━━[/c]""",uid
                                )
                            )
                    else:
                        pass  
#-------------------------------------------------------------#
                if "1200" in data.hex()[0:4] and b"/admin" in data:
                    try:
                        i = re.split("/admin", str(data))[1]
                        if "***" in i:
                            i = i.replace("***", "106")
                        sid = str(i).split("(\\x")[0]
                        json_result = get_available_room(data.hex()[10:])
                        
                        parsed_data = json.loads(json_result)
                        uid = parsed_data["5"]["data"]["1"]["data"]
                        clients.send(
                            self.GenResponsMsg(
                                f"""[C][B][FF0000]╔══════════╗
[FFFFFF]✨ If anyone wants to buy TCP bot  
[FFFFFF]          ⚡ Or purchase access ❤️  
[FFFFFF]                   Just contact me...  
[FF0000]╠══════════╣
[FFD700]⚡ OWNER : [FFFFFF]BANECIPHERXR   
[FFD700]⚡ TELEGRAM : [FFFFFF]@BANECIPHERXR 
[FFD700]✨ Name on Telegram : [FFFFFF]BANECIPHERXR 
[FF0000]╚══════════╝
[FFD700]✨ Developer —͟͞͞ </> BANECIPHER XR ⚡""", uid
                            )
                        )
                    except Exception as e:
                        logging.error(f"Error processing /admin command: {e}. Restarting.")
                        restart_program()                
#-------------------------------------------------------------#
                if "1200" in data.hex()[0:4] and b"/sm" in data:
                    try:
                        # Get the UID of the user who sent the command to send a reply
                        json_result = get_available_room(data.hex()[10:])
                        parsed_data = json.loads(json_result)
                        uid = parsed_data["5"]["data"]["1"]["data"]

                        # Improved Parsing: Use a regular expression to find the ID more reliably
                        match = re.search(r'/sm\s*(\d+)', str(data))
                        
                        if match:
                            player_id_str = match.group(1)

                            # Send an initial confirmation message
                            clients.send(
                                self.GenResponsMsg(
                                    f"[C][B][1E90FF]Request received! Preparing to spam {fix_num(player_id_str)}...", uid
                                )
                            )

                            # --- START OF THE FIX ---
                            # 1. Ensure the bot is not in a squad before starting the spam.
                            # This is the critical step that was missing.
                            logging.info("Resetting bot state to solo before /sm spam.")
                            socket_client.send(self.leave_s())
                            time.sleep(0.5)  # Allow a moment for the leave command to process
                            socket_client.send(self.changes(1)) # Change mode to solo
                            time.sleep(0.5)  # Allow a moment for the mode change
                            # --- END OF THE FIX ---

                            # Create the request packet for the target player
                            invskwad_packet = self.request_join_squad(player_id_str)
                            spam_count = 30  # You can adjust this value

                            # Loop to send the packet multiple times
                            for _ in range(spam_count):
                                socket_client.send(invskwad_packet)
                                sleep(0.1)  # A small delay to prevent server issues

                            # Send a final success message
                            clients.send(
                                self.GenResponsMsg(
                                    f"[C][B][00FF00]Successfully Sent {spam_count} Join Requests!", uid
                                )
                            )

                            # Post-spam cleanup is still good practice.
                            sleep(1)
                            socket_client.send(self.leave_s())
                        
                        else:
                            # Handle cases where the player ID is missing or invalid
                            clients.send(
                                self.GenResponsMsg(
                                    "[C][B][FF0000]Invalid command format. Please use: /sm <player_id>", uid
                                )
                            )

                    except Exception as e:
                        logging.error(f"Error in /sm command: {e}. Restarting.")
                        try:
                            # Attempt to notify the user about the error before restarting
                            json_result = get_available_room(data.hex()[10:])
                            parsed_data = json.loads(json_result)
                            uid = parsed_data["5"]["data"]["1"]["data"]
                            clients.send(self.GenResponsMsg("[C][B][FF0000]An error occurred. Restarting bot...", uid))
                        except:
                            pass 
                        restart_program()
#-------------------------------------------------------------#                                              
                if "1200" in data.hex()[0:4] and b"/x" in data:
                    try:
                        command_split = re.split("/x ", str(data))
                        if len(command_split) > 1:
                            player_id = command_split[1].split('(')[0].strip()
                            if "***" in player_id:
                                player_id = player_id.replace("***", "106")

                            json_result = get_available_room(data.hex()[10:])
                            if not json_result:
                                logging.error("Error: Could not parse incoming packet for /x command.")
                                continue 
                            parsed_data = json.loads(json_result)
                            
                            uid = parsed_data["5"]["data"]["1"]["data"]

                            clients.send(
                                self.GenResponsMsg(
                                    f"[C][B][1E90FF]6 Player Squad Spam Started for {player_id} ...!!!\n",
                                    uid
                                )
                            )

                            def squad_invite_cycle():
                                try:
                                    # Create squad
                                    packetmaker = self.skwad_maker()
                                    socket_client.send(packetmaker)
                                    sleep(0.2)

                                    # Change to 6-player squad
                                    packetfinal = self.changes(5)
                                    socket_client.send(packetfinal)

                                    # Send invite to target player
                                    invitess = self.invite_skwad(player_id)
                                    socket_client.send(invitess)

                                    # Leave squad and go back to solo to repeat the cycle
                                    sleep(0.5)
                                    leavee = self.leave_s()
                                    socket_client.send(leavee)
                                    sleep(0.2)
                                    change_to_solo = self.changes(1)
                                    socket_client.send(change_to_solo)
                                except Exception as e:
                                    logging.error(f"Error inside squad_invite_cycle: {e}")

                            invite_threads = []
                            for _ in range(29): 
                                t = threading.Thread(target=squad_invite_cycle)
                                t.start()
                                invite_threads.append(t)
                                time.sleep(0.2) 

                            for t in invite_threads:
                                t.join() 
                            
                            clients.send(
                                self.GenResponsMsg(
                                    f"[C][B][00FF00]Spam finished for {player_id}!",
                                    uid
                                )
                            )

                    except Exception as e:
                        logging.error(f"An unexpected error occurred in the /x command: {e}. Restarting.")
                        restart_program()                                           
#-------------------------------------------------------------#
                if "1200" in data.hex()[0:4] and b"/3" in data:
                    try:
                        i = re.split("/3", str(data))[1]
                        if "***" in i:
                            i = i.replace("***", "106")
                        sid = str(i).split("(\\x")[0]
                        
                        json_result = get_available_room(data.hex()[10:])
                        parsed_data = json.loads(json_result)
                        uid = parsed_data["5"]["data"]["1"]["data"]

                        packetmaker = self.skwad_maker()
                        socket_client.send(packetmaker)
                        sleep(0.5)

                        packetfinal = self.changes(2)
                        socket_client.send(packetfinal)
                        sleep(0.5)

                        room_data = None
                        if b'(' in data:
                            split_data = data.split(b'/3')
                            if len(split_data) > 1:
                                room_data = split_data[1].split(
                                    b'(')[0].decode().strip().split()
                                if room_data:
                                    iddd = room_data[0]
                                    invitess = self.invite_skwad(iddd)
                                    socket_client.send(invitess)
                                else:
                                    iddd = uid
                                    invitess = self.invite_skwad(iddd)
                                    socket_client.send(invitess)

                        if uid:
                            clients.send(
                                self.GenResponsMsg(
                                    f"""[00FFFF][b][c]╔══⚡ Invite Sent ⚡══╗

[FFFFFF]❤️ Accept the request quickly!\n
[FFFFFF]              3 MAN SQUAD!\n

[FF0000]╚══════════╝

[FFD700]✨ Developer —͟͞͞ </> BANECIPHERXR  ⚡""",
                                    uid
                                )
                            )

                        sleep(5)
                        leavee = self.leave_s()
                        socket_client.send(leavee)
                        sleep(1)
                        change_to_solo = self.changes(1)
                        socket_client.send(change_to_solo)
                    except Exception as e:
                        logging.error(f"Error processing /3 command: {e}. Restarting.")
                        restart_program()
#-------------------------------------------------------------#                                        
                if "1200" in data.hex()[0:4] and b"/4" in data:
                    try:
                        i = re.split("/4", str(data))[1]
                        if "***" in i:
                            i = i.replace("***", "106")
                        sid = str(i).split("(\\x")[0]
                        json_result = get_available_room(data.hex()[10:])
                        parsed_data = json.loads(json_result)

                        packetmaker = self.skwad_maker()
                        socket_client.send(packetmaker)
                        sleep(1)

                        packetfinal = self.changes(3)
                        socket_client.send(packetfinal)

                        room_data = None
                        uid = parsed_data["5"]["data"]["1"]["data"] # Define uid here
                        iddd = uid # Default to sender's id
                        if b'(' in data:
                            split_data = data.split(b'/4')
                            if len(split_data) > 1:
                                room_data = split_data[1].split(
                                    b'(')[0].decode().strip().split()
                                if room_data:
                                    iddd = room_data[0]

                        invitess = self.invite_skwad(iddd)
                        socket_client.send(invitess)

                        if uid:
                            clients.send(
                                self.GenResponsMsg(
                                    f"""[00FFFF][b][c]╔══⚡ Invite Sent ⚡══╗

[FFFFFF]❤️ Accept the request quickly!\n
[FFFFFF]              4 MAN SQUAD!\n

[FF0000]╚══════════╝

[FFD700]✨ Developer —͟͞͞ </> BANECIPHERXR ⚡""",
                                    uid))

                        sleep(5)
                        leavee = self.leave_s()
                        socket_client.send(leavee)
                        sleep(2)
                        change_to_solo = self.changes(1)
                        socket_client.send(change_to_solo)
                    except Exception as e:
                        logging.error(f"Error processing /4 command: {e}. Restarting.")
                        restart_program()                
#-------------------------------------------------------------#                              
                if "1200" in data.hex()[0:4] and b"/5" in data:
                    try:
                        i = re.split("/5", str(data))[1]
                        if "***" in i:
                            i = i.replace("***", "106")
                        sid = str(i).split("(\\x")[0]
                        json_result = get_available_room(data.hex()[10:])
                        parsed_data = json.loads(json_result)

                        packetmaker = self.skwad_maker()
                        socket_client.send(packetmaker)
                        sleep(1)

                        packetfinal = self.changes(4)
                        socket_client.send(packetfinal)

                        room_data = None
                        uid = parsed_data["5"]["data"]["1"]["data"] # Define uid here
                        iddd = uid # Default to sender's id
                        if b'(' in data:
                            split_data = data.split(b'/5')
                            if len(split_data) > 1:
                                room_data = split_data[1].split(
                                    b'(')[0].decode().strip().split()
                                if room_data:
                                    iddd = room_data[0]

                        invitess = self.invite_skwad(iddd)
                        socket_client.send(invitess)

                        if uid:
                            clients.send(
                                self.GenResponsMsg(
                                    f"""[00FFFF][b][c]╔══⚡ Invite Sent ⚡══╗

[FFFFFF]❤️ Accept the request quickly!\n
[FFFFFF]              5 MAN SQUAD!\n

[FF0000]╚══════════╝

[FFD700]✨ Developer —͟͞͞ </> BANECIPHERXR  ⚡""",
                                    uid))

                        sleep(5)
                        leavee = self.leave_s()
                        socket_client.send(leavee)
                        sleep(2)
                        change_to_solo = self.changes(1)
                        socket_client.send(change_to_solo)
                    except Exception as e:
                        logging.error(f"Error processing /5 command: {e}. Restarting.")
                        restart_program()
#-------------------------------------------------------------#                           
                if "1200" in data.hex()[0:4] and b"/6" in data:
                    try:
                        i = re.split("/6", str(data))[1]
                        if "***" in i:
                            i = i.replace("***", "106")
                        sid = str(i).split("(\\x")[0]
                        json_result = get_available_room(data.hex()[10:])
                        parsed_data = json.loads(json_result)
                        packetmaker = self.skwad_maker()
                        socket_client.send(packetmaker)
                        sleep(0.5)
                        packetfinal = self.changes(5)
                        
                        uid = parsed_data["5"]["data"]["1"]["data"]
                        iddd = uid
                        if b'(' in data:
                            split_data = data.split(b'/6')
                            if len(split_data) > 1:
                                room_data = split_data[1].split(
                                    b'(')[0].decode().strip().split()
                                if room_data:
                                    iddd = room_data[0]

                        socket_client.send(packetfinal)
                        invitess = self.invite_skwad(iddd)
                        socket_client.send(invitess)
                        if uid:
                            clients.send(
                                self.GenResponsMsg(
                        f"""[00FFFF][b][c]╔══⚡ Invite Sent ⚡══╗

[FFFFFF]❤️ Accept the request quickly!\n
[FFFFFF]              6 MAN SQUAD!\n

[FF0000]╚══════════╝

[FFD700]✨ Developer —͟͞͞ </> BANECIPHERXR  ⚡""",
                                    uid))

                        sleep(4)
                        leavee = self.leave_s()
                        socket_client.send(leavee)
                        sleep(0.5)
                        change_to_solo = self.changes(1)
                        socket_client.send(change_to_solo)
                    except Exception as e:
                        logging.error(f"Error processing /6 command: {e}. Restarting.")
                        restart_program()
#-------------------------------------------------------------#
                if "1200" in data.hex()[0:4] and b"/change" in data:
                    try:
                        # Get the UID of the user who sent the command to send a reply
                        json_result = get_available_room(data.hex()[10:])
                        parsed_data = json.loads(json_result)
                        uid = parsed_data["5"]["data"]["1"]["data"]

                        # Parse the command to get the desired action (e.g., "6" or "spm")
                        command_parts = data.split(b'/change')[1].split(b'(')[0].decode().strip().split()

                        # Check if an argument was provided
                        if not command_parts:
                            clients.send(
                                self.GenResponsMsg(
                                    "[C][B][FF0000]Usage: /change <size_or_spm>\nExamples:\n/change 6\n/change spm", uid
                                )
                            )
                            continue

                        # The sub-command is the first argument (e.g., '6' or 'spm')
                        sub_command = command_parts[0].lower() # .lower() makes it case-insensitive

                        # --- Handler for the 'spm' sub-command ---
                        if sub_command == "spm":
                            clients.send(
                                self.GenResponsMsg(
                                    f"[C][B][FFA500]Starting team size spam (5-6) for 15 cycles...", uid
                                )
                            )

                            # Loop 15 times to spam the team size change
                            for i in range(15):
                                socket_client.send(self.changes(5)) # Change to 6-player squad
                                time.sleep(0.2)
                                socket_client.send(self.changes(4)) # Change to 5-player squad
                                time.sleep(0.2)

                            clients.send(
                                self.GenResponsMsg(
                                    f"[C][B][00FF00]Team size spam completed!", uid
                                )
                            )
                        
                        # --- Handler for a specific team size number ---
                        elif sub_command.isdigit():
                            team_size = int(sub_command)
                            
                            # Maps the desired team size to the correct parameter for the self.changes() function
                            size_to_param_map = {3: 2, 4: 3, 5: 4, 6: 5}

                            # Check if the requested size is a valid option
                            if team_size not in size_to_param_map:
                                clients.send(
                                    self.GenResponsMsg(
                                        f"[C][B][FF0000]Invalid team size. Please choose 3, 4, 5, or 6.", uid
                                    )
                                )
                                continue
                            
                            change_param = size_to_param_map[team_size]
                            
                            clients.send(
                                self.GenResponsMsg(
                                    f"[C][B][FFFF00]Attempting to change team size to {team_size}...", uid
                                )
                            )

                            # Send the packet to change the team mode
                            socket_client.send(self.changes(change_param))
                            time.sleep(0.5) # Allow time for the change to process

                            clients.send(
                                self.GenResponsMsg(
                                    f"[C][B][00FF00]Successfully changed team mode to a {team_size}-player squad!", uid
                                )
                            )
                        
                        # --- Handler for any other invalid input ---
                        else:
                            clients.send(
                                self.GenResponsMsg(
                                    f"[C][B][FF0000]Invalid command. Use a number (3-6) or 'spm'.", uid
                                )
                            )

                    except Exception as e:
                        logging.error(f"Error processing /change command: {e}. Restarting.")
                        try:
                            json_result = get_available_room(data.hex()[10:])
                            parsed_data = json.loads(json_result)
                            uid = parsed_data["5"]["data"]["1"]["data"]
                            clients.send(self.GenResponsMsg("[C][B][FF0000]An error occurred with /change. Restarting...", uid))
                        except:
                            pass
                        restart_program()
#-------------------------------------------------------------#
                if "1200" in data.hex()[0:4] and b"/team" in data:
                    try:
                        # Decode the incoming data, ignoring errors and removing null characters
                        raw_message = data.decode('utf-8', errors='ignore')
                        cleaned_message = raw_message.replace('\x00', '').strip()
                        
                        # Set a default ID in case one is not provided or is invalid
                        default_id = "2060437760"
                        team_uid = default_id
                        
                        # Use regex to find a valid player ID after the /team command
                        id_match = re.search(r'/team\s*(\d{5,15})\b', cleaned_message)
                        if id_match:
                            # If a match is found, use it as the target UID
                            team_uid = id_match.group(1)
                        
                        # Get the sender's UID to send a response
                        json_result = get_available_room(data.hex()[10:])
                        parsed_data = json.loads(json_result)
                        uid = parsed_data["5"]["data"]["1"]["data"]

                        # Send a confirmation message that the spam is starting
                        clients.send(
                            self.GenResponsMsg(
                                f"[00FF00][b][c]TEAM SPAM STARTED FOR 10 SECONDS ON UID: {fix_num(team_uid)}", 
                                uid
                            )
                        )

                        start_time = time.time()
                        
                        # Run the spam loop for 10 seconds
                        while time.time() - start_time < 10:
                            # Create a squad
                            packetmaker = self.skwad_maker()
                            socket_client.send(packetmaker)
                            sleep(0.05)
                            
                            # Change to 5-player mode
                            packetfinal_5 = self.changes(4)
                            socket_client.send(packetfinal_5)
                            
                            # Send the invite
                            invitess = self.invite_skwad(team_uid)
                            socket_client.send(invitess)

                            sleep(0.05)
                            # Change to 6-player mode
                            packetfinal_6 = self.changes(5)
                            socket_client.send(packetfinal_6)
                        
                        # After the loop finishes, leave the squad
                        leavee = self.leave_s()
                        socket_client.send(leavee)
                        
                        # Send a final confirmation message
                        clients.send(
                            self.GenResponsMsg(
                                f"[00FF00][b][c]TEAM SPAM COMPLETED FOR UID: {fix_num(team_uid)}", 
                                uid
                            )
                        )

                    except Exception as e:
                        # Log the error for debugging
                        logging.error(f"Error in /team command: {e}. Restarting.")
                        
                        # Try to inform the user about the error before restarting
                        try:
                            json_result = get_available_room(data.hex()[10:])
                            parsed_data = json.loads(json_result)
                            uid = parsed_data["5"]["data"]["1"]["data"]
                            clients.send(
                                self.GenResponsMsg(
                                    f"[FF0000]An error occurred in the /team command. The bot will restart.", 
                                    uid
                                )
                            )
                        except:
                            # If sending the message fails, just proceed with the restart
                            pass
                        
                        # Restart the program to ensure stability
                        restart_program()
#-------------------------------------------------------------#                                
                if "1200" in data.hex()[0:4] and b"/status" in data:
                    try:
                        i = re.split("/status", str(data))[1]
                        if "***" in i:
                            i = i.replace("***", "106")
                        sid = str(i).split("(\\x")[0]
                        json_result = get_available_room(data.hex()[10:])
                        parsed_data = json.loads(json_result)
                        uid = parsed_data["5"]["data"]["1"]["data"]
                        split_data = re.split(rb'/status', data)
                        room_data = split_data[1].split(b'(')[0].decode().strip().split()
                        if room_data:
                            player_id = room_data[0]
                            packetmaker = self.createpacketinfo(player_id)
                            socket_client.send(packetmaker)
                            statusinfo1 = True
                            while statusinfo1:
                                if statusinfo == True:
                                    if "IN ROOM" in tempdata:
                                        inforoooom = self.info_room(data22)
                                        socket_client.send(inforoooom)
                                        sleep(0.5)
                                        clients.send(self.GenResponsMsg(f"{tempdata1}", uid))  
                                        tempdata = None
                                        tempdata1 = None
                                        statusinfo = False
                                        statusinfo1 = False
                                    else:
                                        clients.send(self.GenResponsMsg(f"{tempdata}", uid))  
                                        tempdata = None
                                        tempdata1 = None
                                        statusinfo = False
                                        statusinfo1 = False
                        else:
                            clients.send(self.GenResponsMsg("[C][B][FF0000] Please enter a player ID!", uid))  
                    except Exception as e:
                        logging.error(f"Error in /status command: {e}. Restarting.")
                        try:
                            json_result = get_available_room(data.hex()[10:])
                            uid = json.loads(get_available_room(data.hex()[10:]))["5"]["data"]["1"]["data"]
                            clients.send(self.GenResponsMsg("[C][B][FF0000]ERROR! Bot will restart.", uid))
                        except:
                            pass
                        restart_program()
#-------------------------------------------------------------#                             
                if "1200" in data.hex()[0:4] and b"/inv" in data:
                    try:
                        i = re.split("/inv", str(data))[1]
                        if "***" in i:
                            i = i.replace("***", "106")
                        sid = str(i).split("(\\x")[0]
                        json_result = get_available_room(data.hex()[10:])
                        parsed_data = json.loads(json_result)
                        uid = parsed_data["5"]["data"]["1"]["data"]
                        split_data = re.split(rb'/inv', data)
                        room_data = split_data[1].split(b'(')[0].decode().strip().split()
                        if room_data:
                            iddd = room_data[0]
                            numsc1 = "5"

                            if numsc1 is None:
                                clients.send(
                                    self.GenResponsMsg(
                                        f"[C][B] [FF00FF]Please write id and count of the group\n[ffffff]Example : \n/inv 123[c]456[c]78 4\n/inv 123[c]456[c]78 5", uid
                                    )
                                )
                            else:
                                numsc = int(numsc1) - 1
                                if int(numsc1) < 3 or int(numsc1) > 6:
                                    clients.send(
                                        self.GenResponsMsg(
                                            f"[C][B][FF0000] Usage : /inv <uid> <Squad Type>\n[ffffff]Example : \n/inv 12345678 4\n/inv 12345678 5", uid
                                        )
                                    )
                                else:
                                    packetmaker = self.skwad_maker()
                                    socket_client.send(packetmaker)
                                    sleep(1)
                                    packetfinal = self.changes(int(numsc))
                                    socket_client.send(packetfinal)
                                    
                                    invitess = self.invite_skwad(iddd)
                                    socket_client.send(invitess)
                                    iddd1 = parsed_data["5"]["data"]["1"]["data"]
                                    invitessa = self.invite_skwad(iddd1)
                                    socket_client.send(invitessa)
                                    clients.send(
                                self.GenResponsMsg(
                                    f"[C][B][00ff00]Team creation is in progress and the invite has been sent! ", uid
                                )
                            )

                        sleep(5)
                        leavee = self.leave_s()
                        socket_client.send(leavee)
                        sleep(5)
                        change_to_solo = self.changes(1)
                        socket_client.send(change_to_solo)
                        sleep(0.1)
                        clients.send(
                            self.GenResponsMsg(
                                f"[C][B] [FF00FF]Bot is now in solo mode.", uid
                            )
                        )
                    except Exception as e:
                        logging.error(f"Error processing /inv command: {e}. Restarting.")
                        restart_program()
#-------------------------------------------------------------#                        
                if "1200" in data.hex()[0:4] and b"/room" in data:
                    try:
                        i = re.split("/room", str(data))[1] 
                        sid = str(i).split("(\\x")[0]
                        json_result = get_available_room(data.hex()[10:])
                        parsed_data = json.loads(json_result)
                        uid = parsed_data["5"]["data"]["1"]["data"]
                        split_data = re.split(rb'/room', data)
                        room_data = split_data[1].split(b'(')[0].decode().strip().split()
                        if room_data:
                            
                            player_id = room_data[0]
                            if player_id.isdigit():
                                if "***" in player_id:
                                    player_id = rrrrrrrrrrrrrr(player_id)
                                packetmaker = self.createpacketinfo(player_id)
                                socket_client.send(packetmaker)
                                sleep(0.5)
                                if "IN ROOM" in tempdata:
                                    room_id = get_idroom_by_idplayer(data22)
                                    packetspam = self.spam_room(room_id, player_id)
                                    #logging.info(packetspam.hex())
                                    clients.send(
                                        self.GenResponsMsg(
                                            f"[C][B][00ff00]Working on your request for {fix_num(player_id)} ! ", uid
                                        )
                                    )
                                    
                                    
                                    for _ in range(99):

                                        #logging.info(" sending spam to "+player_id)
                                        threading.Thread(target=socket_client.send, args=(packetspam,)).start()
                                    
                                    
                                    
                                    clients.send(
                                        self.GenResponsMsg(
                                            f"[C][B] [00FF00]Request successful! ✅", uid
                                        )
                                    )
                                else:
                                    clients.send(
                                        self.GenResponsMsg(
                                            f"[C][B] [FF00FF]The player is not in a room", uid
                                        )
                                    )      
                            else:
                                clients.send(
                                    self.GenResponsMsg(
                                        f"[C][B] [FF00FF]Please write the player's ID!", uid
                                    )
                                )   

                        else:
                            clients.send(
                                self.GenResponsMsg(
                                    f"[C][B] [FF00FF]Please write the player's ID !", uid
                                )
                            )   
                    except Exception as e:
                        logging.error(f"Error processing /room command: {e}. Restarting.")
                        restart_program()

#-------------------------------------------------------------#          
                if "1200" in data.hex()[0:4] and b"[FFFFF00]BANECIPHER  [ffffff]XR" in data:
                    pass
                else:
                
                    if "1200" in data.hex()[0:4] and b"/spam" in data:
                        try:
                            command_split = re.split("/spam", str(data))
                            if len(command_split) > 1:
                                player_id = command_split[1].split('(')[0].strip()
                                #logging.info(f"Sending Spam To {player_id}")
                                json_result = get_available_room(data.hex()[10:])
                                parsed_data = json.loads(json_result)
                                uid = parsed_data["5"]["data"]["1"]["data"]
                                clients.send(
                                self.GenResponsMsg(
                                    f"{generate_random_color()}Sending friend requests...", uid
                                )
                            )
                                
                                message = send_spam(player_id)
                                #logging.info(message)
                                json_result = get_available_room(data.hex()[10:])
                                parsed_data = json.loads(json_result)
                                uid = parsed_data["5"]["data"]["1"]["data"]
                                
                                clients.send(self.GenResponsMsg(message, uid))
                        except Exception as e:
                            logging.error(f"Error processing /spam command: {e}. Restarting.")
                            restart_program()
#-------------------------------------------------------------#                            
                    if "1200" in data.hex()[0:4] and b"/visit" in data:
                        try:
                            command_split = re.split("/visit", str(data))
                            if len(command_split) > 1:
                                player_id = command_split[1].split('(')[0].strip()

                                #logging.info(f"[C][B]Sending visit To {player_id}")
                                json_result = get_available_room(data.hex()[10:])
                                parsed_data = json.loads(json_result)
                                uid = parsed_data["5"]["data"]["1"]["data"]
                                clients.send(
                    self.GenResponsMsg(
                        f"{generate_random_color()}Sending 1000 visits to {fix_num(player_id)}...", uid
                                    )
                                )
                                
                                message = send_vistttt(player_id)
                                json_result = get_available_room(data.hex()[10:])
                                parsed_data = json.loads(json_result)
                                uid = parsed_data["5"]["data"]["1"]["data"]
                                
                                clients.send(self.GenResponsMsg(message, uid))
                        except Exception as e:
                            logging.error(f"Error processing /visit command: {e}. Restarting.")
                            restart_program()	                           
#-------------------------------------------------------------#           
                    if "1200" in data.hex()[0:4] and b"/info" in data:
                        try:
                            # Extract the sender's ID to send the reply back
                            json_result = get_available_room(data.hex()[10:])
                            parsed_data = json.loads(json_result)
                            sender_id = parsed_data["5"]["data"]["1"]["data"]

                            # Extract the target ID from the user's message
                            command_split = re.split("/info", str(data))
                            if len(command_split) <= 1 or not command_split[1].strip():
                                clients.send(self.GenResponsMsg("[C][B][FF0000] Please provide a player ID after the command.", sender_id))
                                continue

                            # Find the first valid-looking number string in the command text
                            uids = re.findall(r"\b\d{5,15}\b", command_split[1])
                            uid_to_check = uids[0] if uids else ""

                            if not uid_to_check:
                                clients.send(self.GenResponsMsg("[C][B][FF0000] Invalid or missing Player ID.", sender_id))
                                continue
                            
                            clients.send(self.GenResponsMsg(f"[C][B][FFFF00]✅ Request received! Fetching info for {fix_num(uid_to_check)}...", sender_id))
                            time.sleep(0.5)

                            # Call the new info function
                            info_response = newinfo(uid_to_check)
                            
                            if info_response.get('status') != "ok":
                                clients.send(self.GenResponsMsg("[C][B][FF0000]❌ Wrong ID or API error. Please double-check the ID.", sender_id))
                                continue

                            info = info_response['info']

                            # --- Message 1: Basic Account Info ---
                            player_info_msg = (
                                f"[C][B][00FF00]━━「 Player Information 」━━\n"
                                f"[FFA500]• Name: [FFFFFF]{info.get('AccountName', 'N/A')}\n"
                                f"[FFA500]• Level: [FFFFFF]{info.get('AccountLevel', 'N/A')}\n"
                                f"[FFA500]• Likes: [FFFFFF]{fix_num(info.get('AccountLikes', 0))}\n"
                                f"[FFA500]• UID: [FFFFFF]{fix_num(info.get('accountId', 'N/A'))}\n"
                                f"[FFA500]• Region: [FFFFFF]{info.get('AccountRegion', 'N/A')}"
                            )
                            clients.send(self.GenResponsMsg(player_info_msg, sender_id))
                            time.sleep(0.5)

                            # --- Message 2: Rank and Signature ---
                            rank_info_msg = (
                                f"[C][B][00BFFF]━━「 Rank & Status 」━━\n"
                                f"[FFA500]• BR Rank: [FFFFFF]{info.get('BrMaxRank', 'N/A')} ({info.get('BrRankPoint', 0)} pts)\n"
                                f"[FFA500]• CS Rank: [FFFFFF]{info.get('CsMaxRank', 'N/A')} ({info.get('CsRankPoint', 0)} pts)\n"
                                f"[FFA500]• Bio: [FFFFFF]{info.get('signature', 'No Bio').replace('|', ' ')}"
                            )
                            clients.send(self.GenResponsMsg(rank_info_msg, sender_id))
                            time.sleep(0.5)

                            # --- Message 3: Guild Info (only if the player is in a guild) ---
                            if info.get('GuildID') and info.get('GuildID') != "0":
                                guild_info_msg = (
                                    f"[C][B][FFD700]━━「 Guild Information 」━━\n"
                                    f"[FFA500]• Name: [FFFFFF]{info.get('GuildName', 'N/A')}\n"
                                    f"[FFA500]• ID: [FFFFFF]{fix_num(info.get('GuildID', 'N/A'))}\n"
                                    f"[FFA500]• Members: [FFFFFF]{info.get('GuildMember', 0)}/{info.get('GuildCapacity', 0)}\n"
                                    f"[FFA500]• Level: [FFFFFF]{info.get('GuildLevel', 'N/A')}"
                                )
                                clients.send(self.GenResponsMsg(guild_info_msg, sender_id))
                            else:
                                clients.send(self.GenResponsMsg("[C][B][FFD700]Player is not currently in a guild.", sender_id))

                        except Exception as e:
                            logging.error(f"CRITICAL ERROR in /info command: {e}. Restarting bot.")
                            # Attempt to notify the user of the crash before restarting
                            try:
                                json_result = get_available_room(data.hex()[10:])
                                parsed_data = json.loads(json_result)
                                sender_id = parsed_data["5"]["data"]["1"]["data"]
                                clients.send(self.GenResponsMsg("[C][B][FF0000]A critical error occurred. The bot will restart now.", sender_id))
                            except:
                                pass # Ignore if sending the error message also fails
                            restart_program()
#-------------------------------------------------------------#	                    
                    if "1200" in data.hex()[0:4] and b"/likes" in data:
                        try:
                            json_result = get_available_room(data.hex()[10:])
                            parsed_data = json.loads(json_result)
                            uid = parsed_data["5"]["data"]["1"]["data"]
                            clients.send(
                                self.GenResponsMsg(
                                    f"{generate_random_color()}The request is being processed.", uid
                                )
                            )
                            command_split = re.split("/likes", str(data))
                            player_id = command_split[1].split('(')[0].strip()
                            
                            # This part works perfectly with the new function
                            likes_response = send_likes(player_id)
                            message = likes_response['message']
                            clients.send(self.GenResponsMsg(message, uid))

                        except Exception as e:
                            logging.error(f"Error processing /likes command: {e}. Restarting.")
                            restart_program()
#-------------------------------------------------------------#
                    if "1200" in data.hex()[0:4] and b"/help" in data:
                        try:
                            json_result = get_available_room(data.hex()[10:])
                            parsed_data = json.loads(json_result)
                            uid = parsed_data["5"]["data"]["1"]["data"]
                            
                            clients.send(
                                self.GenResponsMsg(
                                        f"""[B][C][FFFF00]✨ BECIPHER PRIVATE BOT✨
[FFFFFF]WELCOME! SEE COMMANDS BELOW 👇

""", uid
                                )
                            )
                            time.sleep(0.2)
                            clients.send(
                                    self.GenResponsMsg(
                                        f"""[C][B][FFFF00]───────────────
[C][B][FF8800] GROUP COMMANDS
[C][B][FFFF00]───────────────

[00FF00]/🙃3  -> [FFFFFF]3-Player Group
[00FF00]/🙃4  -> [FFFFFF]4-Player Group
[00FF00]/🙃5  -> [FFFFFF]5-Player Group
[00FF00]/🙃6  -> [FFFFFF]6-Player Group
[00FF00]/🙃change [3-6]  -> [FFFFFF]change team size
[FFA500]/🙃inv [id] -> [FFFFFF]Invite Any Player""", uid
                                    )
                                )
                            time.sleep(0.2)
                            clients.send(
                                    self.GenResponsMsg(
                                        f"""[C][B][FFFF00]───────────────
[C][B][FF0000] SPAM COMMANDS
[C][B][FFFF00]───────────────

[FF0000]/🙃team [id] -> [FFFFFF]Team size change spam
[FF0000]/🙃spam [id] -> [FFFFFF]Spam Friend Requests
[FF0000]/🙃x [id] -> [FFFFFF]Spam Invite Requests
[FF0000]/🙃sm [id] -> [FFFFFF]Spam Join Requests""", uid
                                    )
                                )
                            time.sleep(0.2)
                            clients.send(
                                    self.GenResponsMsg(
                                        f"""[C][B][FFFF00]───────────────
[C][B][FF0000] ATTACK / LAG COMMANDS
[C][B][FFFF00]───────────────

[FF0000]/🙃attack (team) -> [FFFFFF]Attack Any Team
[FF0000]/🙃start (team) -> [FFFFFF]Force Start a Team""", uid
                                    )
                                )
                            time.sleep(0.2)
                            clients.send(
                                    self.GenResponsMsg(
                                        f"""[C][B][FFFF00]───────────────
[C][B][00CED1] EMOTE-COMMANDS
[C][B][FFFF00]───────────────

[00FF00]/🙃emote (uid) (1-409) -> [FFFFFF]Play any emote without emote id 
[00FF00]/🙃evo (uid) (1-17) -> [FFFFFF]Play max evo gun emote
[00FF00]/🙃play (uid) (emote-id) -> [FFFFFF]Play any emote
[00FF00]/🙃smplay (uid) (emote-id) -> [FFFFFF]spam playing emote """, uid
                                    )
                                )
                            time.sleep(0.2)
                            clients.send(
                                    self.GenResponsMsg(
                                        f"""[C][B][FFFF00]───────────────
[C][B][00CED1] GENERAL COMMANDS
[C][B][FFFF00]───────────────

[00FF00]/🙃likes [id] -> [FFFFFF]Get 100 Likes
[00FF00]/🙃status [id] -> [FFFFFF]Check Player Status
[00FF00]/🙃visit [id] -> [FFFFFF]Increase Visitors""", uid
                                    )
                                )
                            time.sleep(0.2)
                            clients.send(
                                    self.GenResponsMsg(
                                        f"""[C][B][FFFF00]───────────────
[C][B][FFD700] EXTRA COMMANDS
[C][B][FFFF00]───────────────

[00FF00]/🙃ai [word] -> [FFFFFF]Ask Bharat AI
[00FF00]/🙃admin -> [FFFFFF]Know Bot's Admin
                               """, uid
                                    )
                                )
                        except Exception as e:
                            logging.error(f"Error processing /help command: {e}. Restarting.")
                            restart_program()                        
#-------------------------------------------------------------#
                    if "1200" in data.hex()[0:4] and b"/ai" in data:
                        try:
                            i = re.split("/ai", str(data))[1]
                            if "***" in i:
                                i = i.replace("***", "106")
                            sid = str(i).split("(\\x")[0].strip()
                            headers = {"Content-Type": "application/json"}
                            payload = {
                                "contents": [
                                    {
                                        "parts": [
                                            {"text": sid}
                                        ]
                                    }
                                ]
                            }
                            response = requests.post(
                                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyDZvi8G_tnMUx7loUu51XYBt3t9eAQQLYo",
                                headers=headers,
                                json=payload,
                            )
                            if response.status_code == 200:
                                ai_data = response.json()
                                ai_response = ai_data['candidates'][0]['content']['parts'][0]['text']
                                json_result = get_available_room(data.hex()[10:])
                                parsed_data = json.loads(json_result)
                                uid = parsed_data["5"]["data"]["1"]["data"]
                                clients.send(
                                    self.GenResponsMsg(
                                        ai_response, uid
                                    )
                                )
                            else:
                                logging.error(f"Error with AI API: {response.status_code} {response.text}")
                        except Exception as e:
                            logging.error(f"Error processing /ai command: {e}. Restarting.")
                            restart_program()
#-------------------------------------------------------------#
                if '1200' in data.hex()[0:4] and b'/join' in data:
                    try:
                        # Split the incoming data using the new command '/join tc'
                        split_data = re.split(rb'/join', data)
                        json_result = get_available_room(data.hex()[10:])
                        parsed_data = json.loads(json_result)
                        uid = parsed_data['5']['data']['1']['data']
                        
                        # Get the command parts, which should be the room ID
                        command_parts = split_data[1].split(b'(')[0].decode().strip().split()

                        # Check if a room ID was provided
                        if not command_parts:
                            clients.send(self.GenResponsMsg("[C][B][FF0000]Please provide a room code.", uid))
                            continue

                        # The first part of the command is the room ID
                        room_id = command_parts[0]
                        
                        clients.send(
                            self.GenResponsMsg(f"[C][B][32CD32]Attempting to join room: {room_id}", uid)
                        )
                        
                        # Call the join function a single time
                        join_teamcode(socket_client, room_id, key, iv)
                        
                        # Optional: Add a small delay to ensure the join command is processed
                        time.sleep(0.1)

                        clients.send(
                            self.GenResponsMsg(f"[C][B][00FF00]Successfully joined the room.", uid)
                        )

                    except Exception as e:
                        # Updated the error message to reflect the new command name
                        logging.error(f"An error occurred during /join: {e}. Restarting.")
                        restart_program()
#-------------------------------------------------------------#
                if '1200' in data.hex()[0:4] and b'/lag' in data:
                    try:
                        split_data = re.split(rb'/lag', data)
                        json_result = get_available_room(data.hex()[10:])
                        parsed_data = json.loads(json_result)
                        uid = parsed_data['5']['data']['1']['data']
                        command_parts = split_data[1].split(b'(')[0].decode().strip().split()

                        if not command_parts:
                            clients.send(self.GenResponsMsg("[C][B][FF0000]Please provide a code.", uid))
                            continue

                        room_id = command_parts[0]
                        repeat_count = 1
                        if len(command_parts) > 1 and command_parts[1].isdigit():
                            repeat_count = int(command_parts[1])
                        if repeat_count > 3:
                            repeat_count = 3
                        
                        clients.send(
                            self.GenResponsMsg(f"[C][B][32CD32]Starting spam process. Will repeat {repeat_count} time(s).", uid)
                        )
                        
                        for i in range(repeat_count):
                            if repeat_count > 1:
                                clients.send(self.GenResponsMsg(f"[C][B][FFA500]Running batch {i + 1} of {repeat_count}...", uid))

                            for _ in range(11111):
                                join_teamcode(socket_client, room_id, key, iv)
                                time.sleep(0.001)
                                leavee = self.leave_s()
                                socket_client.send(leavee)
                                time.sleep(0.0001)
                            
                            if repeat_count > 1 and i < repeat_count - 1:
                                time.sleep(0.1)

                        clients.send(
                            self.GenResponsMsg(f"[C][B][00FF00]Your order has been confirmed", uid)
                        )
                    except Exception as e:
                        logging.error(f"An error occurred during /lag spam: {e}. Restarting.")
                        restart_program()
#-------------------------------------------------------------#
                if "1200" in data.hex()[0:4] and b"/solo" in data:
                    try:
                        json_result = get_available_room(data.hex()[10:])
                        parsed_data = json.loads(json_result)
                        uid = parsed_data["5"]["data"]["1"]["data"]
                        leavee = self.leave_s()
                        socket_client.send(leavee)
                        sleep(1)
                        change_to_solo = self.changes(1)
                        socket_client.send(change_to_solo)
                        clients.send(
                            self.GenResponsMsg(
                                f"[C][B][00FF00] Exited from the group. ", uid
                            )
                        )
                    except Exception as e:
                        logging.error(f"Error processing /solo command: {e}. Restarting.")
                        restart_program()
#-------------------------------------------------------------#                        
                if '1200' in data.hex()[0:4] and b'/attack' in data:
                    try:
                        split_data = re.split(rb'/attack', data)
                        command_parts = split_data[1].split(b'(')[0].decode().strip().split()
                        json_result = get_available_room(data.hex()[10:])
                        parsed_data = json.loads(json_result)
                        uid = parsed_data['5']['data']['1']['data']

                        if not command_parts:
                            clients.send(self.GenResponsMsg("[C][B][FF0000]With this, you can join and attack any group \n/attack [TeamCode]", uid))
                            continue

                        team_code = command_parts[0]
                        clients.send(
                            self.GenResponsMsg(f"[C][B][FFA500]Join attack has started on Team Code {team_code}...", uid)
                        )

                        start_packet = self.start_autooo()
                        leave_packet = self.leave_s()
                        attack_start_time = time.time()
                        while time.time() - attack_start_time < 45:
                            join_teamcode(socket_client, team_code, key, iv)
                            socket_client.send(start_packet)
                            socket_client.send(leave_packet)
                            time.sleep(0.15)

                        clients.send(
                            self.GenResponsMsg(f"[C][B][00FF00]Double attack on the team is complete! ✅   {team_code}!", uid)
                        )

                    except Exception as e:
                        logging.error(f"An error occurred in /attack command: {e}. Restarting.")
                        restart_program()
#-------------------------------------------------------------#
                if "1200" in data.hex()[0:4] and b"/emote" in data:
                    try:
                        # --- START: Load Emotes from JSON file ---
                        emote_map = {}
                        try:
                            # This will open and read the emotes.json file.
                            # Make sure emotes.json is in the same folder as your app.py file!
                            with open('emotes.json', 'r') as f:
                                emotes_data = json.load(f)
                                # This loop converts the data from the file into the dictionary format the bot needs.
                                for emote_entry in emotes_data:
                                    emote_map[emote_entry['Number']] = emote_entry['Id']
                        
                        except FileNotFoundError:
                            logging.error("CRITICAL: emotes.json file not found! The /emote command is disabled.")
                            # If the file doesn't exist, inform the user.
                            json_result = get_available_room(data.hex()[10:])
                            uid_sender = json.loads(json_result)["5"]["data"]["1"]["data"]
                            clients.send(self.GenResponsMsg(
                                "[C][B][FF0000]Error: emotes.json file is missing. Please contact the admin.", uid_sender
                            ))
                            continue # Stop processing the command
                        
                        except (json.JSONDecodeError, KeyError):
                            logging.error("CRITICAL: emotes.json is formatted incorrectly! The /emote command is disabled.")
                            # If the file is broken or has the wrong format, inform the user.
                            json_result = get_available_room(data.hex()[10:])
                            uid_sender = json.loads(json_result)["5"]["data"]["1"]["data"]
                            clients.send(self.GenResponsMsg(
                                "[C][B][FF0000]Error: Emote data file is corrupted. Please contact the admin.", uid_sender
                            ))
                            continue # Stop processing the command
                        # --- END: Load Emotes from JSON file ---

                        # Get the sender's UID to send replies
                        json_result = get_available_room(data.hex()[10:])
                        parsed_data = json.loads(json_result)
                        uid_sender = parsed_data["5"]["data"]["1"]["data"]

                        # Parse the command parts
                        command_parts = data.split(b'/emote')[1].split(b'(')[0].decode().strip().split()
                        
                        if len(command_parts) < 2:
                            clients.send(self.GenResponsMsg(
                                f"[C][B][FF0000]Usage: /emote <target_id> <emote_number>", uid_sender
                            ))
                            continue

                        emote_choice = command_parts[-1]
                        target_ids = command_parts[:-1]
                        
                        # Dynamically check if the chosen emote number is valid
                        if emote_choice not in emote_map:
                            max_emote_number = len(emote_map)
                            clients.send(self.GenResponsMsg(
                                f"[C][B][FF0000]Invalid emote number. Please use a number between 1 and {max_emote_number}.", uid_sender
                            ))
                            continue
                        
                        emote_id_to_send = emote_map[emote_choice]

                        clients.send(self.GenResponsMsg(
                            f"[C][B][00FF00]Sending emote #{emote_choice} to {len(target_ids)} player(s)...", uid_sender
                        ))
                        
                        # Loop through all provided target IDs
                        for target_id in target_ids:
                            if target_id.isdigit() and emote_id_to_send.isdigit():
                                emote_packet = self.send_emote(target_id, emote_id_to_send)
                                socket_client.send(emote_packet)
                                time.sleep(0.1)
                        
                        clients.send(self.GenResponsMsg(
                            f"[C][B][00FF00]Emote command finished successfully!", uid_sender
                        ))

                    except Exception as e:
                        logging.error(f"Error processing /emote command: {e}. Restarting.")
                        try:
                            json_result = get_available_room(data.hex()[10:])
                            uid = json.loads(json_result)["5"]["data"]["1"]["data"]
                            clients.send(self.GenResponsMsg("[C][B][FF0000]An error occurred with /emote. Restarting...", uid))
                        except:
                            pass
                        restart_program()
#-------------------------------------------------------------#                                
                if "1200" in data.hex()[0:4] and b"/evo" in data:
                    try:
                        # Step 1: Get the sender's UID for replies
                        json_result = get_available_room(data.hex()[10:])
                        parsed_data = json.loads(json_result)
                        uid_sender = parsed_data["5"]["data"]["1"]["data"]

                        # Step 2: Parse the command parts safely
                        command_parts = data.split(b'/evo')[1].split(b'(')[0].decode().strip().split()

                        # Step 3: Validate the number of arguments
                        if len(command_parts) < 2:
                            clients.send(self.GenResponsMsg("[C][B][FF0000]Usage: /evo <player_id> <number>", uid_sender))
                            continue
                        
                        # Step 4: Assign arguments robustly
                        # The last item is the emote choice, the first is the target ID.
                        evo_choice = command_parts[-1] 
                        target_id = command_parts[0]

                        # Step 5: Define the mapping of choices to emote IDs
                        evo_emotes = {
                            "1": "909000063",   # AK
                            "2": "909000068",   # SCAR
                            "3": "909000075",   # 1st MP40
                            "4": "909040010",   # 2nd MP40
                            "5": "909000081",   # 1st M1014
                            "6": "909039011",   # 2nd M1014
                            "7": "909000085",   # XM8
                            "8": "909000090",   # Famas
                            "9": "909000098",   # UMP
                            "10": "909035007",  # M1887
                            "11": "909042008",  # Woodpecker
                            "12": "909041005",  # Groza
                            "13": "909033001",  # M4A1
                            "14": "909038010",  # Thompson
                            "15": "909038012",  # G18
                            "16": "909045001",  # Parafal
                            "17": "909049010"   # P90
                        }
                        emote_id = evo_emotes.get(evo_choice)

                        # Step 6: Validate the chosen number. If it's not in the dictionary, emote_id will be None.
                        if not emote_id:
                            clients.send(self.GenResponsMsg(f"[C][B][FF0000]Invalid choice: {evo_choice}. Please use a number from 1-17.", uid_sender))
                            continue

                        # Step 7: Validate IDs and send the action packet
                        if target_id.isdigit() and emote_id.isdigit():
                            # Create the game action packet
                            emote_packet = self.send_emote(target_id, emote_id)
                            # Send the action to the game server
                            socket_client.send(emote_packet)
                            time.sleep(0.1)
                            
                            # Send a chat confirmation back to the user
                            clients.send(self.GenResponsMsg(f"[C][B][00FF00]EVO emote #{evo_choice} sent to {target_id}!", uid_sender))
                        else:
                            clients.send(self.GenResponsMsg("[C][B][FF0000]Invalid Player ID provided.", uid_sender))

                    except Exception as e:
                        # Consistent error handling with restart
                        logging.error(f"Error processing /evo command: {e}. Restarting.")
                        try:
                            # Attempt to notify the user about the error before restarting
                            json_result = get_available_room(data.hex()[10:])
                            parsed_data = json.loads(json_result)
                            uid = parsed_data["5"]["data"]["1"]["data"]
                            clients.send(self.GenResponsMsg("[C][B][FF0000]An error occurred. Restarting bot...", uid))
                        except:
                            pass 
                        restart_program()
#-------------------------------------------------------------#                                 
                if "1200" in data.hex()[0:4] and b'/play' in data:
                    try:
                        json_result = get_available_room(data.hex()[10:])
                        parsed_data = json.loads(json_result)
                        uid_sender = parsed_data["5"]["data"]["1"]["data"]

                        # Command format: @a <target_id1> [target_id2...] <emote_id>
                        command_parts = data.split(b'/play')[1].split(b'(')[0].decode().strip().split()
                        if len(command_parts) < 2:
                            clients.send(self.GenResponsMsg("[C][B][FF0000]Usage: /play <target_id> <emote_id>", uid_sender))
                            continue

                        emote_id = command_parts[-1]
                        target_ids = command_parts[:-1]

                        clients.send(self.GenResponsMsg(f"[C][B][00FF00]Activating emote {emote_id} for {len(target_ids)} player(s)...", uid_sender))

                        for target_id in target_ids:
                            if target_id.isdigit() and emote_id.isdigit():
                                emote_packet = self.send_emote(target_id, emote_id)
                                socket_client.send(emote_packet) # Send action to online socket
                                time.sleep(0.1) # Small delay between packets
                        
                        clients.send(self.GenResponsMsg(f"[C][B][00FF00]Emote command finished!", uid_sender))

                    except Exception as e:
                        logging.error(f"Error processing /🙂play command: {e}")
                        try:
                            uid_sender = json.loads(get_available_room(data.hex()[10:]))["5"]["data"]["1"]["data"]
                            clients.send(self.GenResponsMsg("[C][B][FF0000]Error processing /🙂play command.", uid_sender))
                        except:
                            pass                
#-------------------------------------------------------------#                                                
                if "1200" in data.hex()[0:4] and b'/smplay' in data:
                    try:
                        json_result = get_available_room(data.hex()[10:])
                        parsed_data = json.loads(json_result)
                        uid_sender = parsed_data["5"]["data"]["1"]["data"]

                        # Command format: @b <target_id1> [target_id2...] <emote_id>
                        command_parts = data.split(b'/smplay')[1].split(b'(')[0].decode().strip().split()
                        if len(command_parts) < 2:
                            clients.send(self.GenResponsMsg("[C][B][FF0000]Usage: /smplay <target_id> <emote_id>", uid_sender))
                            continue

                        emote_id = command_parts[-1]
                        target_ids = command_parts[:-1]

                        clients.send(self.GenResponsMsg(f"[C][B][FF0000]ATTACKING with emote {emote_id} on {len(target_ids)} player(s)!", uid_sender))

                        # Loop for repeating the emote quickly
                        for _ in range(200): # Repeats 200 times
                            for target_id in target_ids:
                                if target_id.isdigit() and emote_id.isdigit():
                                    emote_packet = self.send_emote(target_id, emote_id)
                                    socket_client.send(emote_packet) # Send action to online socket
                            time.sleep(0.08) # Fast repeat speed

                        clients.send(self.GenResponsMsg(f"[C][B][00FF00]Emote attack finished!", uid_sender))

                    except Exception as e:
                        logging.error(f"Error processing /🙂smplay command: {e}")
                        try:
                            uid_sender = json.loads(get_available_room(data.hex()[10:]))["5"]["data"]["1"]["data"]
                            clients.send(self.GenResponsMsg("[C][B][FF0000]Error processing /🙂smplay command.", uid_sender))
                        except:
                            pass                
#-------------------------------------------------------------#                                                
                if "1200" in data.hex()[0:4] and b"/start" in data:
                    try:
                        split_data = re.split(rb'/start', data)
                        json_result = get_available_room(data.hex()[10:])
                        parsed_data = json.loads(json_result)
                        uid = parsed_data['5']['data']['1']['data']
                        command_parts = split_data[1].split(b'(')[0].decode().strip().split()

                        if not command_parts:
                            clients.send(self.GenResponsMsg("[C][B][FF0000]Please provide a team code.", uid))
                            continue

                        team_code = command_parts[0]
                        spam_count = 20
                        if len(command_parts) > 1 and command_parts[1].isdigit():
                            spam_count = int(command_parts[1])
                        if spam_count > 50:
                            spam_count = 50

                        clients.send(
                            self.GenResponsMsg(f"[C][B][FFA500]Joining lobby to force start...", uid)
                        )
                        join_teamcode(socket_client, team_code, key, iv)
                        time.sleep(2)
                        clients.send(
                            self.GenResponsMsg(f"[C][B][FF0000]Spamming start command {spam_count} times!", uid)
                        )
                        start_packet = self.start_autooo()
                        for _ in range(spam_count):
                            socket_client.send(start_packet)
                            time.sleep(0.2)
                        leave_packet = self.leave_s()
                        socket_client.send(leave_packet)
                        clients.send(
                            self.GenResponsMsg(f"[C][B][00FF00]Force start process finished.", uid)
                        )
                    except Exception as e:
                        logging.error(f"An error occurred in /start command: {e}. Restarting.")
                        restart_program()
#-------------------------------------------------------------#                        
                if "1200" in data.hex()[0:4] and b"/snd" in data:
                    try:
                        i = re.split("/snd", str(data))[1]
                        if "***" in i:
                            i = i.replace("***", "106")
                        sid = str(i).split("(\\x")[0]
                        json_result = get_available_room(data.hex()[10:])
                        parsed_data = json.loads(json_result)
                        uid = parsed_data["5"]["data"]["1"]["data"]
                        split_data = re.split(rb'/add', data)
                        room_data = split_data[1].split(b'(')[0].decode().strip().split()
                        if room_data:
                            iddd = room_data[0]
                            numsc1 = room_data[1] if len(room_data) > 1 else None

                            if numsc1 is None:
                                clients.send(
                                    self.GenResponsMsg(
                                        f"[C][B] [FF00FF]Please write id and count of the group\n[ffffff]Example : \n/snd 123[c]456[c]78 4\n/snd 123[c]456[c]78 5", uid
                                    )
                                )
                            else:
                                numsc = int(numsc1) - 1
                                if int(numsc1) < 3 or int(numsc1) > 6:
                                    clients.send(
                                        self.GenResponsMsg(
                                            f"[C][B][FF0000] Usage : /snd <uid> <Squad Type>\n[ffffff]Example : \n/add 12345678 4\n/add 12345678 5", uid
                                        )
                                    )
                                else:
                                    packetmaker = self.skwad_maker()
                                    socket_client.send(packetmaker)
                                    sleep(1)
                                    packetfinal = self.changes(int(numsc))
                                    socket_client.send(packetfinal)
                                    
                                    invitess = self.invite_skwad(iddd)
                                    socket_client.send(invitess)
                                    iddd1 = parsed_data["5"]["data"]["1"]["data"]
                                    invitessa = self.invite_skwad(iddd1)
                                    socket_client.send(invitessa)
                                    clients.send(
                                        self.GenResponsMsg(
                                            f"[C][B][00ff00]- Accept The Invite Quickly ! ", uid
                                        )
                                    )
                                    leaveee1 = True
                                    while leaveee1:
                                        if leaveee == True:
                                            #logging.info("Leave")
                                            leavee = self.leave_s()
                                            sleep(5)
                                            socket_client.send(leavee)   
                                            leaveee = False
                                            leaveee1 = False
                                            clients.send(
                                                self.GenResponsMsg(
                                                    f"[C][B] [FF00FF]success !", uid
                                                )
                                            )    
                                        if pleaseaccept == True:
                                            #logging.info("Leave")
                                            leavee = self.leave_s()
                                            socket_client.send(leavee)   
                                            leaveee1 = False
                                            pleaseaccept = False
                                            clients.send(
                                                self.GenResponsMsg(
                                                    f"[C][B] [FF00FF]Please accept the invite", uid
                                                )
                                            )   
                        else:
                            clients.send(
                                self.GenResponsMsg(
                                    f"[C][B] [FF00FF]Please write id and count of the group\n[ffffff]Example : \n/inv 123[c]456[c]78 4\n/inv 123[c]456[c]78 5", uid
                                )
                            )
                    except Exception as e:
                        logging.error(f"Error processing /🙂snd command: {e}. Restarting.")
                        restart_program()
            # --- START: Added for error handling ---
            except Exception as e:
                logging.critical(f"A critical unhandled error occurred in the main connect loop: {e}. The bot will restart.")
                restart_program()
            # --- END: Added for error handling ---

	                    
                    
    def parse_my_message(self, serialized_data):
        MajorLogRes = MajorLoginRes_pb2.MajorLoginRes()
        MajorLogRes.ParseFromString(serialized_data)
        
        timestamp = MajorLogRes.kts
        key = MajorLogRes.ak
        iv = MajorLogRes.aiv
        BASE64_TOKEN = MajorLogRes.token
        timestamp_obj = Timestamp()
        timestamp_obj.FromNanoseconds(timestamp)
        timestamp_seconds = timestamp_obj.seconds
        timestamp_nanos = timestamp_obj.nanos
        combined_timestamp = timestamp_seconds * 1_000_000_000 + timestamp_nanos
        return combined_timestamp, key, iv, BASE64_TOKEN

    def GET_PAYLOAD_BY_DATA(self,JWT_TOKEN , NEW_ACCESS_TOKEN,date):
        token_payload_base64 = JWT_TOKEN.split('.')[1]
        token_payload_base64 += '=' * ((4 - len(token_payload_base64) % 4) % 4)
        decoded_payload = base64.urlsafe_b64decode(token_payload_base64).decode('utf-8')
        decoded_payload = json.loads(decoded_payload)
        NEW_EXTERNAL_ID = decoded_payload['external_id']
        SIGNATURE_MD5 = decoded_payload['signature_md5']
        now = datetime.now()
        now =str(now)[:len(str(now))-7]
        formatted_time = date
        payload = bytes.fromhex("1a13323032352d30372d33302031313a30323a3531220966726565206669726528013a07312e3131382e31422c416e64726f6964204f5320372e312e32202f204150492d323320284e32473438482f373030323530323234294a0848616e6468656c645207416e64726f69645a045749464960c00c68840772033332307a1f41524d7637205646507633204e454f4e20564d48207c2032343635207c203480019a1b8a010f416472656e6f2028544d292036343092010d4f70656e474c20455320332e319a012b476f6f676c657c31663361643662372d636562342d343934622d383730622d623164616364373230393131a2010c3139372e312e31322e313335aa0102656eb201203939366136323964626364623339363462653662363937386635643831346462ba010134c2010848616e6468656c64ca011073616d73756e6720534d2d473935354eea014066663930633037656239383135616633306134336234613966363031393531366530653463373033623434303932353136643064656661346365663531663261f00101ca0207416e64726f6964d2020457494649ca03203734323862323533646566633136343031386336303461316562626665626466e003daa907e803899b07f003bf0ff803ae088004999b078804daa9079004999b079804daa907c80403d204262f646174612f6170702f636f6d2e6474732e667265656669726574682d312f6c69622f61726de00401ea044832303837663631633139663537663261663465376665666630623234643964397c2f646174612f6170702f636f6d2e6474732e667265656669726574682d312f626173652e61706bf00403f804018a050233329a050a32303139313138363933a80503b205094f70656e474c455332b805ff7fc00504e005dac901ea0507616e64726f6964f2055c4b71734854394748625876574c6668437950416c52526873626d43676542557562555551317375746d525536634e30524f3751453141486e496474385963784d614c575437636d4851322b7374745279377830663935542b6456593d8806019006019a060134a2060134b2061e40001147550d0c074f530b4d5c584d57416657545a065f2a091d6a0d5033")
        payload = payload.replace(b"2025-07-30 11:02:51", str(now).encode())
        payload = payload.replace(b"ff90c07eb9815af30a43b4a9f6019516e0e4c703b44092516d0defa4cef51f2a", NEW_ACCESS_TOKEN.encode("UTF-8"))
        payload = payload.replace(b"996a629dbcdb3964be6b6978f5d814db", NEW_EXTERNAL_ID.encode("UTF-8"))
        payload = payload.replace(b"7428b253defc164018c604a1ebbfebdf", SIGNATURE_MD5.encode("UTF-8"))
        PAYLOAD = payload.hex()
        PAYLOAD = encrypt_api(PAYLOAD)
        PAYLOAD = bytes.fromhex(PAYLOAD)
        whisper_ip, whisper_port, online_ip, online_port = self.GET_LOGIN_DATA(JWT_TOKEN , PAYLOAD)
        return whisper_ip, whisper_port, online_ip, online_port
    
    def dec_to_hex(ask):
        ask_result = hex(ask)
        final_result = str(ask_result)[2:]
        if len(final_result) == 1:
            final_result = "0" + final_result
            return final_result
        else:
            return final_result
    def convert_to_hex(PAYLOAD):
        hex_payload = ''.join([f'{byte:02x}' for byte in PAYLOAD])
        return hex_payload
    def convert_to_bytes(PAYLOAD):
        payload = bytes.fromhex(PAYLOAD)
        return payload
    def GET_LOGIN_DATA(self, JWT_TOKEN, PAYLOAD):
        url = "https://client.ind.freefiremobile.com/GetLoginData"
        headers = {
            'Expect': '100-continue',
            'Authorization': f'Bearer {JWT_TOKEN}',
            'X-Unity-Version': '2018.4.11f1',
            'X-GA': 'v1 1',
            'ReleaseVersion': 'Ob51',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)',
            'Host': 'clientbp.common.ggbluefox.com',
            'Connection': 'close',
            'Accept-Encoding': 'gzip, deflate, br',
        }
        
        max_retries = 3
        attempt = 0

        while attempt < max_retries:
            try:
                response = requests.post(url, headers=headers, data=PAYLOAD,verify=False)
                response.raise_for_status()
                x = response.content.hex()
                json_result = get_available_room(x)
                parsed_data = json.loads(json_result)
                #logging.info(parsed_data)
                
                whisper_address = parsed_data['32']['data']
                online_address = parsed_data['14']['data']
                online_ip = online_address[:len(online_address) - 6]
                whisper_ip = whisper_address[:len(whisper_address) - 6]
                online_port = int(online_address[len(online_address) - 5:])
                whisper_port = int(whisper_address[len(whisper_address) - 5:])
                return whisper_ip, whisper_port, online_ip, online_port
            
            except requests.RequestException as e:
                logging.error(f"Request failed: {e}. Attempt {attempt + 1} of {max_retries}. Retrying...")
                attempt += 1
                time.sleep(2)

        logging.critical("Failed to get login data after multiple attempts. Restarting.")
        restart_program() # Changed to restart if it fails completely
        return None, None

    def guest_token(self,uid , password):
        url = "https://100067.connect.garena.com/oauth/guest/token/grant"
        headers = {"Host": "100067.connect.garena.com","User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 10;en;EN;)","Content-Type": "application/x-www-form-urlencoded","Accept-Encoding": "gzip, deflate, br","Connection": "close",}
        data = {"uid": f"{uid}","password": f"{password}","response_type": "token","client_type": "2","client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3","client_id": "100067",}
        response = requests.post(url, headers=headers, data=data)
        data = response.json()
        NEW_ACCESS_TOKEN = data['access_token']
        NEW_OPEN_ID = data['open_id']
        OLD_ACCESS_TOKEN = "ff90c07eb9815af30a43b4a9f6019516e0e4c703b44092516d0defa4cef51f2a"
        OLD_OPEN_ID = "996a629dbcdb3964be6b6978f5d814db"
        time.sleep(0.2)
        data = self.TOKEN_MAKER(OLD_ACCESS_TOKEN , NEW_ACCESS_TOKEN , OLD_OPEN_ID , NEW_OPEN_ID,uid)
        return(data)
        
    def TOKEN_MAKER(self,OLD_ACCESS_TOKEN , NEW_ACCESS_TOKEN , OLD_OPEN_ID , NEW_OPEN_ID,id):
        headers = {
                       'X-Unity-Version': '2018.4.11f1',
            'ReleaseVersion': 'Ob51',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-GA': 'v1 1',
            'Content-Length': '928',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
            'Host': 'loginbp.ggblueshark.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }
        data = bytes.fromhex('1a13323032352d30372d33302031313a30323a3531220966726565206669726528013a07312e3131382e31422c416e64726f6964204f5320372e312e32202f204150492d323320284e32473438482f373030323530323234294a0848616e6468656c645207416e64726f69645a045749464960c00c68840772033332307a1f41524d7637205646507633204e454f4e20564d48207c2032343635207c203480019a1b8a010f416472656e6f2028544d292036343092010d4f70656e474c20455320332e319a012b476f6f676c657c31663361643662372d636562342d343934622d383730622d623164616364373230393131a2010c3139372e312e31322e313335aa0102656eb201203939366136323964626364623339363462653662363937386635643831346462ba010134c2010848616e6468656c64ca011073616d73756e6720534d2d473935354eea014066663930633037656239383135616633306134336234613966363031393531366530653463373033623434303932353136643064656661346365663531663261f00101ca0207416e64726f6964d2020457494649ca03203734323862323533646566633136343031386336303461316562626665626466e003daa907e803899b07f003bf0ff803ae088004999b078804daa9079004999b079804daa907c80403d204262f646174612f6170702f636f6d2e6474732e667265656669726574682d312f6c69622f61726de00401ea044832303837663631633139663537663261663465376665666630623234643964397c2f646174612f6170702f636f6d2e6474732e667265656669726574682d312f626173652e61706bf00403f804018a050233329a050a32303139313138363933a80503b205094f70656e474c455332b805ff7fc00504e005dac901ea0507616e64726f6964f2055c4b71734854394748625876574c6668437950416c52526873626d43676542557562555551317375746d525536634e30524f3751453141486e496474385963784d614c575437636d4851322b7374745279377830663935542b6456593d8806019006019a060134a2060134b2061e40001147550d0c074f530b4d5c584d57416657545a065f2a091d6a0d5033')
        data = data.replace(OLD_OPEN_ID.encode(),NEW_OPEN_ID.encode())
        data = data.replace(OLD_ACCESS_TOKEN.encode() , NEW_ACCESS_TOKEN.encode())
        hex = data.hex()
        d = encrypt_api(data.hex())
        Final_Payload = bytes.fromhex(d)
        URL = "https://loginbp.ggblueshark.com/MajorLogin"

        RESPONSE = requests.post(URL, headers=headers, data=Final_Payload,verify=False)
        
        combined_timestamp, key, iv, BASE64_TOKEN = self.parse_my_message(RESPONSE.content)
        if RESPONSE.status_code == 200:
            if len(RESPONSE.text) < 10:
                return False
            whisper_ip, whisper_port, online_ip, online_port =self.GET_PAYLOAD_BY_DATA(BASE64_TOKEN,NEW_ACCESS_TOKEN,1)
            self.key = key
            self.iv = iv
            #logging.info(key, iv)
            return(BASE64_TOKEN, key, iv, combined_timestamp, whisper_ip, whisper_port, online_ip, online_port)
        else:
            return False
    
    def time_to_seconds(hours, minutes, seconds):
        return (hours * 3600) + (minutes * 60) + seconds

    def seconds_to_hex(seconds):
        return format(seconds, '04x')
    
    def extract_time_from_timestamp(timestamp):
        dt = datetime.fromtimestamp(timestamp)
        h = dt.hour
        m = dt.minute
        s = dt.second
        return h, m, s
    
    def get_tok(self):
        global g_token
        token_data = self.guest_token(self.id, self.password)
        if not token_data:
            logging.critical("Failed to get token data from guest_token. Restarting.")
            restart_program()

        token, key, iv, Timestamp, whisper_ip, whisper_port, online_ip, online_port = token_data
        g_token = token
        #logging.info(f"{whisper_ip}, {whisper_port}")
        try:
            decoded = jwt.decode(token, options={"verify_signature": False})
            account_id = decoded.get('account_id')
            encoded_acc = hex(account_id)[2:]
            hex_value = dec_to_hex(Timestamp)
            time_hex = hex_value
            BASE64_TOKEN_ = token.encode().hex()
            logging.info(f"Token decoded and processed. Account ID: {account_id}")
        except Exception as e:
            logging.error(f"Error processing token: {e}. Restarting.")
            restart_program()

        try:
            head = hex(len(encrypt_packet(BASE64_TOKEN_, key, iv)) // 2)[2:]
            length = len(encoded_acc)
            zeros = '00000000'

            if length == 9:
                zeros = '0000000'
            elif length == 8:
                zeros = '00000000'
            elif length == 10:
                zeros = '000000'
            elif length == 7:
                zeros = '000000000'
            else:
                logging.warning('Unexpected length encountered')
            head = f'0115{zeros}{encoded_acc}{time_hex}00000{head}'
            final_token = head + encrypt_packet(BASE64_TOKEN_, key, iv)
            logging.info("Final token constructed successfully.")
        except Exception as e:
            logging.error(f"Error constructing final token: {e}. Restarting.")
            restart_program()
        token = final_token
        self.connect(token, 'anything', key, iv, whisper_ip, whisper_port, online_ip, online_port)
        
      
        return token, key, iv
        
with open('bot.txt', 'r') as file:
    data = json.load(file)
ids_passwords = list(data.items())
def run_client(id, password):
    logging.info(f"Starting client for ID: {id}")
    client = FF_CLIENT(id, password)
    # The start method is inherited from threading.Thread and calls the run() method
    # The logic is handled within the FF_CLIENT class itself upon instantiation.
    # No need to call client.start() as it's not defined to do anything special here.
    
max_range = 300000
num_clients = len(ids_passwords)
num_threads = 1
start = 0
end = max_range
step = (end - start) // num_threads
threads = []

# --- START: Modified for robust execution and restart ---
if __name__ == "__main__":
    while True: # This loop ensures the script will always try to restart on a major crash.
        try:
            logging.info("Main execution block started.")
            # Your original threading logic
            for i in range(num_threads):
                ids_for_thread = ids_passwords[i % num_clients]
                id_val, password_val = ids_for_thread
                # The FF_CLIENT init starts the connection logic, which is run in a new thread inside the connect method.
                # The primary thread for each client is created inside its `connect` method.
                # This main thread's purpose is to kick off the clients.
                run_client(id_val, password_val)
                time.sleep(3) # Stagger client startups

            # Keep the main script alive by joining the threads that were created.
            # The threads list is populated inside the connect method.
            logging.info(f"All {len(threads)} client threads initiated. Main thread will now wait.")
            for thread in threads:
                thread.join()

        except KeyboardInterrupt:
            logging.info("Shutdown signal received. Exiting.")
            break
        except Exception as e:
            logging.critical(f"A critical error occurred in the main execution block: {e}")
            logging.info("Restarting the entire application in 5 seconds...")
            time.sleep(5)
            # The restart_program() call will replace this process, so the loop continues in a new instance.
            restart_program()