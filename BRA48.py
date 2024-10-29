import requests
import tkinter as tk
from tkinter import messagebox, font as tkfont
import folium
import webbrowser
import os

# Global variables to store latitude and longitude
lat, lon = None, None

def get_ip_info():
    global lat, lon  # Use global variables to store coordinates
    api_url = "https://ipapi.co/json/"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        
        # Extract latitude and longitude
        lat = data.get('latitude', 'N/A')  # Default to provided coordinates
        lon = data.get('longitude', 'N/A')

        # Update labels in the table format
        ip_label.config(text=data.get('ip', 'N/A'))
        city_label.config(text=data.get('city', 'N/A'))
        region_label.config(text=data.get('region', 'N/A'))
        country_label.config(text=data.get('country', 'N/A'))
        postal_label.config(text=data.get('postal', 'N/A'))
        isp_label.config(text=data.get('org', 'N/A'))
        asn_label.config(text=data.get('asn', 'N/A'))

        # Hide the fetch button
        fetch_button.pack_forget()

        # Show the map button
        map_button.pack(pady=10)  # Make the map button visible

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to retrieve IP information: {e}")

def create_map():
    # Create a folium map centered at the location
    map_center = [lat, lon]
    ip_map = folium.Map(location=map_center, zoom_start=15)

    # Add a marker for the location
    folium.Marker(location=map_center, popup="Location", icon=folium.Icon(color='blue')).add_to(ip_map)

    # Save the map to an HTML file
    map_file = "ip_location_map.html"
    ip_map.save(map_file)

    # Open the map in a web browser
    webbrowser.open('file://' + os.path.realpath(map_file))

# Function to create a rounded button style
def create_rounded_button(master, text, command, **kwargs):
    button = tk.Button(master, text=text, command=command, **kwargs)
    button.config(relief="flat", highlightthickness=0)  
    button.pack()
    return button

# Set up the GUI
root = tk.Tk()
root.title("IP Address Information")
root.geometry("800x600")  # Set the window size
root.configure(bg="#f0f0f0")  # Set background color

# Set a custom font with increased size
custom_font = tkfont.Font(family="Helvetica", size=25)  

# Create a frame for the main content
main_frame = tk.Frame(root, bg="#f0f0f0", padx=45, pady=35)
main_frame.pack(expand=True, fill=tk.BOTH)

# Create a frame for displaying results
result_frame = tk.Frame(main_frame, bg="#ffffff", bd=2, relief="groove", padx=10, pady=10)
result_frame.pack(expand=True, fill=tk.BOTH, pady=10)

# Create labels for the table headers
headers = ["Field", "Value"]
for col, header in enumerate(headers):
    header_label = tk.Label(result_frame, text=header, font=(custom_font.cget("family"), 16, 'bold'), bg="#ffffff")
    header_label.grid(row=0, column=col, padx=10, pady=5, sticky="ew")  # Sticky for horizontal expansion

# Create labels to display IP information with initial values
ip_label = tk.Label(result_frame, text="N/A", justify="left", bg="#ffffff", font=custom_font)
city_label = tk.Label(result_frame, text="N/A", justify="left", bg="#ffffff", font=custom_font)
region_label = tk.Label(result_frame, text="N/A", justify="left", bg="#ffffff", font=custom_font)
country_label = tk.Label(result_frame, text="N/A", justify="left", bg="#ffffff", font=custom_font)
postal_label = tk.Label(result_frame, text="N/A", justify="left", bg="#ffffff", font=custom_font)
isp_label = tk.Label(result_frame, text="N/A", justify="left", bg="#ffffff", font=custom_font)
asn_label = tk.Label(result_frame, text="N/A", justify="left", bg="#ffffff", font=custom_font)

# Place the information labels in the grid
labels = [
    "IP Address", 
    "City", 
    "Region", 
    "Country", 
    "Postal Code", 
    "ISP", 
    "ASN"
]

for row, label in enumerate(labels, start=1):
    label_field = tk.Label(result_frame, text=label, bg="#ffffff", font=custom_font)
    label_field.grid(row=row, column=0, padx=10, pady=5, sticky="ew")  # Sticky for horizontal expansion
    # Add corresponding value label
    value_label = ip_label if label == "IP Address" else (
        city_label if label == "City" else (
        region_label if label == "Region" else (
        country_label if label == "Country" else (
        postal_label if label == "Postal Code" else (
        isp_label if label == "ISP" else asn_label
    )))))
    value_label.grid(row=row, column=1, padx=10, pady=5, sticky="ew")  # Sticky for horizontal expansion

# Set initial values for the labels
ip_label.config(text="Loading...")
city_label.config(text="Loading...")
region_label.config(text="Loading...")
country_label.config(text="Loading...")
postal_label.config(text="Loading...")
isp_label.config(text="Loading...")
asn_label.config(text="Loading...")

# Create a button to fetch IP information
fetch_button = create_rounded_button(main_frame, "Get IP Info", get_ip_info, bg="#007BFF", fg="white", font=custom_font, padx=10, pady=5)

# Create a button to see the map location (initially hidden)
map_button = create_rounded_button(main_frame, "See Map Location", create_map, bg="#28A745", fg="white", font=custom_font, padx=10, pady=5)
map_button.pack_forget()  # Hide the button initially

# Run the GUI main loop
root.mainloop()
