import tkinter as tk
from tkinter import messagebox, filedialog
import speedtest
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import csv
from datetime import datetime
import requests

def get_public_ip_info():
    """Fetch public IP and ISP details."""
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        return data.get("ip", "Unknown"), data.get("org", "Unknown ISP")
    except:
        return "Unknown", "Unknown ISP"

def run_speed_test():
    """Perform an internet speed test and update the GUI."""
    start_button.config(state=tk.DISABLED)
    status_label.config(text="Testing... Please wait")
    app.update()
    
    try:
        speed_test = speedtest.Speedtest()
        speed_test.get_best_server()
        
        download_speed = speed_test.download() / 1_000_000  # Convert to Mbps
        upload_speed = speed_test.upload() / 1_000_000  # Convert to Mbps
        ping_time = speed_test.results.ping
        
        download_label.config(text=f"Download Speed: {download_speed:.2f} Mbps")
        upload_label.config(text=f"Upload Speed: {upload_speed:.2f} Mbps")
        ping_label.config(text=f"Ping: {ping_time:.2f} ms")
        status_label.config(text="Test Completed!")
        
        ip_address, isp_name = get_public_ip_info()
        ip_label.config(text=f"IP Address: {ip_address}")
        isp_label.config(text=f"ISP: {isp_name}")
        
        update_chart(download_speed, upload_speed, ping_time)
        save_test_results(download_speed, upload_speed, ping_time, ip_address, isp_name)
    except Exception as error:
        messagebox.showerror("Error", f"Failed to test speed:\n{error}")
        status_label.config(text="Error")
    
    start_button.config(state=tk.NORMAL)

def update_chart(download, upload, ping):
    """Update the bar chart with the latest test results."""
    chart_axis.clear()
    categories = ['Download', 'Upload', 'Ping']
    values = [download, upload, ping]
    chart_axis.bar(categories, values, color=['green', 'blue', 'red'])
    chart_axis.set_ylabel("Speed (Mbps / ms)")
    chart_axis.set_title("Internet Speed Test Results")
    chart_canvas.draw()

def save_test_results(download, upload, ping, ip, isp):
    """Save test results in JSON and CSV formats."""
    result = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Download": f"{download:.2f} Mbps",
        "Upload": f"{upload:.2f} Mbps",
        "Ping": f"{ping:.2f} ms",
        "IP": ip,
        "ISP": isp
    }
    
    with open("speed_test_history.json", "a") as json_file:
        json.dump(result, json_file)
        json_file.write("\n")
    
    with open("speed_test_history.csv", "a", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(result.values())

def export_results():
    """Export results to a user-selected JSON or CSV file."""
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json"), ("CSV Files", "*.csv")])
    if not file_path:
        return
    
    with open("speed_test_history.json", "r") as json_file:
        data = json_file.readlines()
    
    if file_path.endswith(".json"):
        with open(file_path, "w") as file:
            file.writelines(data)
    elif file_path.endswith(".csv"):
        with open(file_path, "w", newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Date", "Download", "Upload", "Ping", "IP", "ISP"])
            for line in data:
                result = json.loads(line)
                writer.writerow(result.values())
    messagebox.showinfo("Export", "Results exported successfully!")

# Create GUI
app = tk.Tk()
app.title("Internet Speed Test")
app.geometry("600x600")
app.configure(bg="#222")  # Dark mode

# UI Elements
tk.Label(app, text="Internet Speed Test", font=("Arial", 16, "bold"), fg="white", bg="#222").pack(pady=10)
status_label = tk.Label(app, text="Click Start to Test", font=("Arial", 12), fg="white", bg="#222")
status_label.pack(pady=5)

download_label = tk.Label(app, text="Download Speed: - Mbps", font=("Arial", 12), fg="white", bg="#222")
download_label.pack(pady=5)

upload_label = tk.Label(app, text="Upload Speed: - Mbps", font=("Arial", 12), fg="white", bg="#222")
upload_label.pack(pady=5)

ping_label = tk.Label(app, text="Ping: - ms", font=("Arial", 12), fg="white", bg="#222")
ping_label.pack(pady=5)

ip_label = tk.Label(app, text="IP Address: -", font=("Arial", 12), fg="white", bg="#222")
ip_label.pack(pady=5)

isp_label = tk.Label(app, text="ISP: -", font=("Arial", 12), fg="white", bg="#222")
isp_label.pack(pady=5)

# Buttons
start_button = tk.Button(app, text="Start Test", font=("Arial", 12, "bold"), command=run_speed_test, bg="#444", fg="white")
start_button.pack(pady=10)

export_button = tk.Button(app, text="Export Results", font=("Arial", 12, "bold"), command=export_results, bg="#555", fg="white")
export_button.pack(pady=10)

# Matplotlib Graph
fig, chart_axis = plt.subplots(figsize=(4, 3))
chart_canvas = FigureCanvasTkAgg(fig, master=app)
chart_canvas.get_tk_widget().pack()

# Run GUI
app.mainloop()