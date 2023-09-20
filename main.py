import tkinter as tk
from tkinter import ttk
import requests  # Import the requests library
import configparser
import json
import cv2
from pyzbar import pyzbar
import qrcode
from PIL import Image, ImageTk

class AppStyle:
    @staticmethod
    def configure_styles():
        # Create a ttk style
        style = ttk.Style()
        
        # Configure the label style
        style.configure('TLabel', background='black', foreground='white', font=('Helvetica', 12))
        
        # Configure the entry style
        style.configure('TEntry', fieldbackground='lightgray', foreground='black', font=('Helvetica', 12))
        
        # Configure the button style
        style.configure('TButton', background='blue', foreground='white', font=('Helvetica', 12))

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")
        

        # Create labels and entry widgets for email and password
        self.email_label = ttk.Label(root, text="Email:")
        self.email_label.pack(pady=10)
        self.email_entry = ttk.Entry(root)
        self.email_entry.pack(pady=5)
        
        self.password_label = ttk.Label(root, text="Password:")
        self.password_label.pack(pady=10)
        self.password_entry = ttk.Entry(root, show="*")
        self.password_entry.pack(pady=5)
        
        # Create a login button
        self.login_button = ttk.Button(root, text="Login", command=self.login)
        self.login_button.pack(pady=20)
        
        # Check if there's a token in config.ini and open the dashboard if it exists
        if self.check_token():
            self.root.destroy()
            # Close the login window
            self.open_dashboard() 
            
            
    def check_token(self):
                # Check if there's a token in config.ini
               config = configparser.ConfigParser()
               config.read('config.ini')
    
               if 'Token' in config and 'access_token' in config['Token']:
        # Check if the value associated with 'access_token' is not empty
                return bool(config['Token']['access_token'].strip())
               else:
                 return False
    def open_dashboard(self):
                root = tk.Tk()
                root.geometry("800x600")
                DashboardApp(root)
                root.mainloop()  
                     

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        # Define the API URL
        api_url = "https://iidtrackbackend-production.up.railway.app/api/token/"
        
        # Create a payload for the POST request
        payload = {
            "email": email,
            "password": password
        }
        
        try:
        # Convert the payload to a JSON string
            json_payload = json.dumps(payload)            
            # Send a POST request with the JSON data
            response = requests.post(api_url, data=json_payload, headers={"Content-Type": "application/json"})
            jsonresponse = response.json()  # Parse the JSON response
            print(jsonresponse['access'])
            
            if response.status_code == 200:
                token = response.json().get("access")
                # Store the token in the configuration file
                config = configparser.ConfigParser()
                config.read('config.ini')
                config['Token']['access_token'] = token
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
                
                self.root.destroy()
                self.open_dashboard()  
           
            else:
                print("Login failed. Please check your credentials.")
                
                     
        except Exception as e:
            print("An error occurred:", str(e))
            
              
def close_processing_window():
    global processing_window
    if processing_window and processing_window.winfo_exists():
        processing_window.destroy()         
def button_click_handler(motordata,window_to_destroy):
    # Do something with the medicine_names list
    data = motordata
    for  item in data:
        print(item)
    window_to_destroy.destroy()
    
   
    
    global processing_window
    processing_window = tk.Toplevel()
    processing_window.title("Processing...")
    processing_window.geometry("500x400") 
    processing_label = tk.Label(processing_window, text="Processing, please wait...")
    processing_label.pack()

    # Close the processing window after 3 seconds
    window_to_destroy.after(3000, close_processing_window)
    print("Button clicked with medicine_names:", motordata)
    
    
    
class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("800x600")  # Set the window size
        
        # Create a ttk style
        self.style = ttk.Style()
        self.style.configure('TLabel', background='black', foreground='white', font=('Helvetica', 12))
        self.style.configure('TEntry', fieldbackground='black', foreground='white', font=('Helvetica', 12))
        self.style.configure('TButton', background='black', foreground='white', font=('Helvetica', 12))
        
        # Create a gradient background frame
        self.background_frame = GradientFrame(self.root, color1="blue", color2="pink")
        self.background_frame.pack(fill="both", expand=True)
        
        # Add a logo image to the top left corner
        self.logo_image = Image.open("logo.png")  # Replace with your logo image file path
        self.logo_image = self.logo_image.resize((100, 100))  # Resize the logo
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = ttk.Label(self.background_frame, image=self.logo_photo)
        self.logo_label.image = self.logo_photo
        self.logo_label.grid(row=0, column=0, padx=20, pady=20, sticky="nw")
        
        # Create a Scan QR Code button
        self.scan_qr_code_button = ttk.Button(self.background_frame, text="Scan QR Code", command=self.scan_qr_code)
        self.scan_qr_code_button.grid(row=1, column=0, padx=20, pady=20, sticky="w")
        
        # Create a label to display the scanned QR code data
        self.qr_code_label = ttk.Label(self.background_frame, text="QR Code Data: ", font=('Helvetica', 12))
        self.qr_code_label.grid(row=2, column=0, padx=20, pady=20, sticky="w")
        
        # Create an input field for entering a numeric ID
        self.id_label = ttk.Label(self.background_frame, text="Enter Numeric ID:", font=('Helvetica', 12))
        self.id_label.grid(row=3, column=0, padx=20, pady=20, sticky="w")
        self.id_entry = ttk.Entry(self.background_frame)
        self.id_entry.grid(row=4, column=0, padx=20, pady=20, sticky="w")
        
        # Create a Submit button
        self.submit_button = ttk.Button(self.background_frame, text="Submit", command=self.submit_id)
        self.submit_button.grid(row=5, column=0, padx=20, pady=20, sticky="w")
   
        self.root = root
        self.root.title("Dashboard")
        self.root.configure(bg='black')
        self.style = ttk.Style()
        self.style.configure('TLabel', background='black', foreground='white', font=('Helvetica', 12))
        self.style.configure('TEntry', fieldbackground='black', foreground='white', font=('Helvetica', 12))
        self.style.configure('TButton', background='black', foreground='white', font=('Helvetica', 12))
        
    def scan_qr_code(self):
        # Open the camera
        cap = cv2.VideoCapture(1)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            # Convert the frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect QR codes in the frame
            decoded_objects = pyzbar.decode(gray)

            for obj in decoded_objects:
                # Extract QR code data
                qr_data = obj.data.decode('utf-8')
                
                # Display the QR code data on the label
                self.qr_code_label.config(text="QR Code Data: " + qr_data)
            
            # Display the camera feed in a window
            cv2.imshow("QR Code Scanner", frame)

            # Check for the 'q' key to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the camera and close all windows
        cap.release()
        cv2.destroyAllWindows()
        
    def submit_id(self):
        id = self.id_entry.get()
        
        # Get the access token from the configuration file
        access_token = self.get_access_token()
        
        if access_token:
            # Make a POST request with the numeric ID and token
            api_url = f"https://iidtrackbackend-production.up.railway.app/api/getprescription/{id}"  # Corrected URL formatting Replace with your API endpoint
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            try:
                response = requests.get(api_url,  headers=headers)
                if response.status_code == 200:
                    # Assuming the response contains JSON data
                    response_data = response.json()
                    medicine_names = response_data.get("medicine_names", [])
                    prescriptiondetails = response_data.get("prescription_details", [])
                    pateintname = prescriptiondetails['patient_name']
                    motordata = prescriptiondetails['medicines']
                    print(motordata)
                    # Display the response data or perform any other actions here
                    print(response_data)
                    medicine_window = tk.Toplevel(self.root)
                    medicine_window.title("Medicine Data")
                    medicine_window.geometry("600x500")  
                    tree = ttk.Treeview(medicine_window, columns=("Medicine Name"))
                    tree.heading('#1', text = f"patientname = {pateintname}")
                    tree.heading("#2", text="Medicine Name")
                    tree.pack()
                    for medicine_name in medicine_names:
                      tree.insert("", "end", values=(medicine_name))
                      
                    button = tk.Button(medicine_window, text="Get the Medicines",
                           command=lambda: button_click_handler(motordata, medicine_window))
                    button.pack()  
                 
                else:
                    print(f"Failed to submit ID. Status code: {response.status_code}")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
        else:
            print("Access token not found. Please log in first.")
    
    def get_access_token(self):
        # Retrieve the access token from the configuration file
        config = configparser.ConfigParser()
        config.read('config.ini')
        if 'Token' in config and 'access_token' in config['Token']:
            return config['Token']['access_token']
        else:
            return None

        
        
        
class GradientFrame(tk.Canvas):
    def __init__(self, parent, color1, color2):
        tk.Canvas.__init__(self, parent, borderwidth=0, highlightthickness=0)
        self.color1 = color1
        self.color2 = color2
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        width = self.winfo_width()
        height = self.winfo_height()
        mid = width / 2
        self.create_rectangle(0, 0, mid, height, fill=self.color1, width=0)
        self.create_rectangle(mid, 0, width, height, fill=self.color2, width=0)        


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    AppStyle.configure_styles()
    login_app = LoginApp(root)
    root.mainloop()
