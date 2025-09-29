import tkinter as tk
from tkinter import ttk, messagebox
import threading

class BluetoothAIGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_gui()
        
    def setup_gui(self):
        self.root.title("Bluetooth AI Fix Master")
        self.root.geometry("800x600")
        
        # Header
        header = tk.Frame(self.root, bg='#0047AB', height=80)
        header.pack(fill=tk.X)
        
        title = tk.Label(header, text="Bluetooth AI Fix Master", 
                        font=('Arial', 20, 'bold'), fg='white', bg='#0047AB')
        title.pack(pady=20)
        
        # Scan button
        scan_btn = tk.Button(self.root, text="Scan Devices", 
                           command=self.scan_devices, font=('Arial', 14))
        scan_btn.pack(pady=20)
        
        # Devices list
        self.devices_tree = ttk.Treeview(self.root, columns=('Name', 'MAC', 'Status'))
        self.devices_tree.heading('Name', text='Device Name')
        self.devices_tree.heading('MAC', text='MAC Address')
        self.devices_tree.heading('Status', text='Status')
        self.devices_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
    def scan_devices(self):
        def scan():
            # Simulate scanning
            devices = [
                ('Sony WH-1000XM4', '04:5F:01:02:03', 'Available'),
                ('Apple AirPods Pro', 'DC:56:04:05:06', 'Connected')
            ]
            self.root.after(0, self.update_devices, devices)
        
        threading.Thread(target=scan).start()
    
    def update_devices(self, devices):
        for item in self.devices_tree.get_children():
            self.devices_tree.delete(item)
        
        for device in devices:
            self.devices_tree.insert('', tk.END, values=device)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = BluetoothAIGUI()
    app.run()
