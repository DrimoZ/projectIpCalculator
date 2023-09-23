import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Create a Tkinter window
root = tk.Tk()
root.title("Image from URL")

# Function to display an image from a URL
def display_image():
    # Get the URL from the Entry widget
    url = url_entry.get()

    try:
        # Fetch the image from the URL
        response = requests.get(url)
        img_data = response.content

        # Convert the image data into a PIL Image
        img = Image.open(BytesIO(img_data))

        # Create a Tkinter PhotoImage object from the PIL Image
        img_tk = ImageTk.PhotoImage(img)

        # Display the image in a Label widget
        image_label.config(image=img_tk)
        image_label.image = img_tk

    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")

# Create an Entry widget for entering the image URL
url_label = tk.Label(root, text="Enter Image URL:")
url_label.pack()

url_entry = tk.Entry(root)
url_entry.pack()

# Create a Button to fetch and display the image
fetch_button = tk.Button(root, text="Fetch Image", command=display_image)
fetch_button.pack()

# Create a Label to display the image
image_label = tk.Label(root)
image_label.pack()

# Create a Label to display error messages, if any
result_label = tk.Label(root, fg="red")
result_label.pack()

# Start the Tkinter main loop
root.mainloop()