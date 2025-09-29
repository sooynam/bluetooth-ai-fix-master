# src/gui_interface.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time

class BluetoothAIGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.ai_fixer = None
        self.devices = []
        
        self.setup_gui()
        self.load_ai_fixer()
        
    def load_ai_fixer(self):
        """AI fixer load karein background mein"""
        def load():
            try:
                from ai_bluetooth_fix import AIBluetoothFixer
                self.ai_fixer = AIBluetoothFixer()
                self.root.after(0, self.update_status, "✅ AI System Ready")
            except Exception as e:
                self.root.after(0, self.update_status, f"❌ AI System Failed: {e}")
        
        threading.Thread(target=load, daemon=True).start()
        self.update_status("🔄 Loading AI System...")
    
    def setup_gui(self):
        """Main GUI setup karein"""
        self.root.title("Bluetooth AI Fix Master")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Header
        header_frame = tk.Frame(self.root, bg='#0047AB', height=100)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        title_label = tk.Label(
            header_frame,
            text="Bluetooth AI Fix Master",
            font=('Arial', 24, 'bold'),
            fg='white',
            bg='#0047AB'
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            header_frame,
            text="AI-Powered Bluetooth Problem Solver",
            font=('Arial', 12),
            fg='white',
            bg='#0047AB'
        )
        subtitle_label.pack(pady=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="🔄 Initializing...")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                            relief=tk.SUNKEN, anchor=tk.W, bg='#e0e0e0')
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel - Controls
        left_frame = tk.Frame(main_frame, bg='#f0f0f0')
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Scan section
        scan_frame = tk.LabelFrame(left_frame, text="Device Scanner", 
                                 font=('Arial', 12, 'bold'), bg='#f0f0f0')
        scan_frame.pack(fill=tk.X, pady=10)
        
        self.scan_btn = tk.Button(
            scan_frame,
            text="🔍 Scan Bluetooth Devices",
            command=self.start_scanning,
            bg='#0047AB',
            fg='white',
            font=('Arial', 11, 'bold'),
            width=20,
            height=2
        )
        self.scan_btn.pack(pady=10)
        
        # AI Actions section
        ai_frame = tk.LabelFrame(left_frame, text="AI Actions", 
                               font=('Arial', 12, 'bold'), bg='#f0f0f0')
        ai_frame.pack(fill=tk.X, pady=10)
        
        self.diagnose_btn = tk.Button(
            ai_frame,
            text="🤖 Run AI Diagnosis",
            command=self.run_diagnosis,
            bg='#FF6B6B',
            fg='white',
            font=('Arial', 11),
            width=20,
            height=2
        )
        self.diagnose_btn.pack(pady=5)
        
        self.fix_btn = tk.Button(
            ai_frame,
            text="🔧 Auto Fix Issues",
            command=self.auto_fix,
            bg='#4ECDC4',
            fg='white',
            font=('Arial', 11),
            width=20,
            height=2
        )
        self.fix_btn.pack(pady=5)
        
        # Right panel - Results
        right_frame = tk.Frame(main_frame, bg='#f0f0f0')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Devices list
        devices_frame = tk.LabelFrame(right_frame, text="Found Devices",
                                    font=('Arial', 12, 'bold'), bg='#f0f0f0')
        devices_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview for devices
        self.devices_tree = ttk.Treeview(devices_frame, columns=('Name', 'MAC', 'Status', 'Signal'), show='headings')
        self.devices_tree.heading('Name', text='Device Name')
        self.devices_tree.heading('MAC', text='MAC Address')
        self.devices_tree.heading('Status', text='Status')
        self.devices_tree.heading('Signal', text='Signal')
        
        # Configure columns
        self.devices_tree.column('Name', width=200)
        self.devices_tree.column('MAC', width=150)
        self.devices_tree.column('Status', width=100)
        self.devices_tree.column('Signal', width=80)
        
        # Scrollbar for treeview
        tree_scroll = ttk.Scrollbar(devices_frame, orient=tk.VERTICAL, command=self.devices_tree.yview)
        self.devices_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.devices_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Results section
        results_frame = tk.LabelFrame(right_frame, text="AI Diagnosis Results",
                                    font=('Arial', 12, 'bold'), bg='#f0f0f0')
        results_frame.pack(fill=tk.BOTH, pady=10)
        
        self.results_text = scrolledtext.ScrolledText(
            results_frame, 
            height=12, 
            wrap=tk.WORD,
            font=('Consolas', 10)
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Initially disable buttons
        self.diagnose_btn.config(state=tk.DISABLED)
        self.fix_btn.config(state=tk.DISABLED)
    
    def update_status(self, message):
        """Status update karein"""
        self.status_var.set(message)
    
    def start_scanning(self):
        """Device scanning start karein"""
        if not self.ai_fixer:
            messagebox.showerror("Error", "AI system not ready yet!")
            return
            
        self.scan_btn.config(state=tk.DISABLED, text="🔄 Scanning...")
        self.update_status("🔍 Scanning for Bluetooth devices...")
        
        threading.Thread(target=self.scan_devices, daemon=True).start()
    
    def scan_devices(self):
        """Bluetooth devices scan karein"""
        try:
            self.devices = self.ai_fixer.scan_devices()
            self.root.after(0, self.update_devices_list)
            self.root.after(0, self.update_status, f"✅ Found {len(self.devices)} devices")
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Scan Error", f"Scan failed: {str(e)}"))
            self.root.after(0, self.update_status, "❌ Scan failed")
        finally:
            self.root.after(0, self.scan_btn.config, {"state": tk.NORMAL, "text": "🔍 Scan Bluetooth Devices"})
    
    def update_devices_list(self):
        """Devices list update karein"""
        # Clear existing items
        for item in self.devices_tree.get_children():
            self.devices_tree.delete(item)
        
        # Add new devices
        for device in self.devices:
            status = "Connected" if device.get('connected', False) else "Available"
            signal = f"{device.get('signal_strength', 0)} dBm"
            
            self.devices_tree.insert('', tk.END, values=(
                device['name'],
                device['mac_address'],
                status,
                signal
            ))
        
        # Enable diagnose button if devices found
        if self.devices:
            self.diagnose_btn.config(state=tk.NORMAL)
            self.fix_btn.config(state=tk.NORMAL)
    
    def run_diagnosis(self):
        """AI diagnosis run karein"""
        selected_item = self.devices_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a device first")
            return
        
        device_index = self.devices_tree.index(selected_item[0])
        device_data = self.devices[device_index]
        
        self.diagnose_btn.config(state=tk.DISABLED, text="🔬 Diagnosing...")
        self.update_status(f"🔬 Diagnosing {device_data['name']}...")
        
        threading.Thread(target=self.perform_diagnosis, args=(device_data,), daemon=True).start()
    
    def perform_diagnosis(self, device_data):
        """Perform actual diagnosis"""
        try:
            diagnosis = self.ai_fixer.diagnose_device(device_data)
            self.root.after(0, self.display_diagnosis, diagnosis)
            self.root.after(0, self.update_status, f"✅ Diagnosis complete for {device_data['name']}")
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Diagnosis Error", f"Diagnosis failed: {str(e)}"))
            self.root.after(0, self.update_status, "❌ Diagnosis failed")
        finally:
            self.root.after(0, self.diagnose_btn.config, {"state": tk.NORMAL, "text": "🤖 Run AI Diagnosis"})
    
    def display_diagnosis(self, diagnosis):
        """Diagnosis results display karein"""
        device = diagnosis['device']
        
        results = f"🤖 AI DIAGNOSIS REPORT\n"
        results += "=" * 50 + "\n\n"
        results += f"📱 Device: {device['name']}\n"
        results += f"🔗 MAC: {device['mac_address']}\n"
        results += f"📶 Signal: {device.get('signal_strength', 'N/A')} dBm\n"
        results += f"⚡ Battery: {device.get('battery_level', 'N/A')}%\n\n"
        
        results += f"🎯 Confidence Score: {diagnosis['confidence_score']:.2f}\n"
        results += f"⏱️ Estimated Time: {diagnosis['estimated_time']}\n"
        results += f"⚠️ Risk Level: {diagnosis['risk_level'].upper()}\n\n"
        
        results += "🔍 DETECTED ISSUES:\n"
        results += "-" * 30 + "\n"
        
        if diagnosis['detected_issues']:
            for i, issue in enumerate(diagnosis['detected_issues'], 1):
                results += f"{i}. {issue['description']}\n"
                results += f"   Confidence: {issue['confidence']:.2f} | Severity: {issue['severity'].upper()}\n\n"
        else:
            results += "✅ No issues detected! Device is working optimally.\n\n"
        
        results += "🛠️ SUGGESTED FIXES:\n"
        results += "-" * 30 + "\n"
        
        if diagnosis['suggested_fixes']:
            for i, fix in enumerate(diagnosis['suggested_fixes'], 1):
                results += f"{i}. {fix['description']}\n"
                results += f"   Success Rate: {fix['success_rate']:.2f} | Time: {fix['estimated_time']}\n\n"
        else:
            results += "✅ No fixes needed at this time.\n"
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, results)
    
    def auto_fix(self):
        """Auto fix issues"""
        selected_item = self.devices_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a device first")
            return
        
        device_index = self.devices_tree.index(selected_item[0])
        device_data = self.devices[device_index]
        
        # For demo, show a simple fix
        result = self.ai_fixer.apply_fix("reset_bluetooth_stack", device_data)
        messagebox.showinfo("Auto Fix", f"Applied fix: {result['message']}")
    
    def run(self):
        """GUI run karein"""
        self.root.mainloop()

if __name__ == "__main__":
    app = BluetoothAIGUI()
    app.run()
