import tkinter as tk
from tkinter import ttk, filedialog
import socket
import threading
import os

print(""" 
███╗░░██╗░██████╗████████╗
████╗░██║██╔════╝╚══██╔══╝
██╔██╗██║╚█████╗░░░░██║░░░
██║╚████║░╚═══██╗░░░██║░░░
██║░╚███║██████╔╝░░░██║░░░
╚═╝░░╚══╝╚═════╝░░░░╚═╝░░░ """)


class PortScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Port Scanner")
        self.root.geometry("400x400")
        
        self.target_label = ttk.Label(root, text="Target Host or IP:")
        self.target_label.pack(pady=10)
        
        self.target_entry = ttk.Entry(root, width=30)
        self.target_entry.pack()
        
        self.port_range_label = ttk.Label(root, text="Port Range:")
        self.port_range_label.pack(pady=10)
        
        self.start_port_entry = ttk.Entry(root, width=6)
        self.start_port_entry.insert(0, "1")
        self.start_port_entry.pack(side=tk.LEFT, padx=10)
        
        self.to_label = ttk.Label(root, text="to")
        self.to_label.pack(side=tk.LEFT)
        
        self.end_port_entry = ttk.Entry(root, width=6)
        self.end_port_entry.insert(0, "100")
        self.end_port_entry.pack(side=tk.LEFT, padx=10)
        
        self.scan_button = ttk.Button(root, text="Scan Ports", command=self.start_scan)
        self.scan_button.pack(pady=10)
        
        self.export_button = ttk.Button(root, text="Export Ports Info", command=self.export_ports_info)
        self.export_button.pack(pady=10)
        
        self.result_label = ttk.Label(root, text="Open Ports:")
        self.result_label.pack()
        
        self.show_info_var = tk.BooleanVar()
        self.show_info_var.set(False)  # Initially, don't show info
        
        self.toggle_info_button = ttk.Checkbutton(root, text="Show Info", variable=self.show_info_var, command=self.toggle_info)
        self.toggle_info_button.pack(pady=5)
        
        self.result_text = tk.Text(root, height=10, width=40)
        self.result_text.pack(pady=10)
        
    def start_scan(self):
        target_host = self.target_entry.get()
        start_port = int(self.start_port_entry.get())
        end_port = int(self.end_port_entry.get())
        
        self.result_text.delete(1.0, tk.END)  # Clear previous results
        
        for port in range(start_port, end_port + 1):
            threading.Thread(target=self.scan_port, args=(target_host, port)).start()
    
    def scan_port(self, target_host, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)  # Adjust the timeout as needed
                result = s.connect_ex((target_host, port))
                if result == 0:
                    self.result_text.insert(tk.END, f"Port {port} is open\n")
                    if self.show_info_var.get():
                        service_name = self.get_service_name(port)
                        self.result_text.insert(tk.END, f" - Service: {service_name}\n")
                s.close()
        except (socket.timeout, ConnectionRefusedError):
            pass
        except socket.error as e:
            self.result_text.insert(tk.END, f"Error occurred while scanning port {port}: {e}\n")

    def toggle_info(self):
        if self.show_info_var.get():
            self.result_label.config(text="Open Ports and Service Info:")
        else:
            self.result_label.config(text="Open Ports:")
    
    def get_service_name(self, port):
        # You can implement a service name lookup here using a dictionary or a service lookup library
        # For simplicity, we'll just return the port number as the service name.
        return str(port)

    def export_ports_info(self):
        info = self.result_text.get(1.0, tk.END)
        if not info.strip():
            return  # No info to export
        
        target_host = self.target_entry.get()
        
        # Ask the user for the folder to save the file
        folder_selected = filedialog.askdirectory(title="Select Folder to Save Info")
        
        if folder_selected:
            # Construct the file path with the target host as the file name
            file_name = f"{target_host}_ports_info.txt"
            file_path = os.path.join(folder_selected, file_name)
            
            # Write the info to the file
            with open(file_path, "w") as file:
                file.write(info)
            
            # Inform the user about the successful export
            tk.messagebox.showinfo("Export Successful", f"Ports information saved to {file_path}")

def main():
    root = tk.Tk()
    app = PortScannerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
