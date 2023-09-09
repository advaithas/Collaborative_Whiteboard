import socket
import threading
import tkinter as tk

# Define host and port
HOST = '127.0.0.1'
PORT = 8000

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))

# Create GUI window
window = tk.Tk()
window.title("Collaborative Whiteboard")

# Create canvas widget for drawing
canvas = tk.Canvas(window, width=500, height=500, bg='white')
canvas.pack()

# Function to handle drawing on canvas
def draw(event):
    x, y = event.x, event.y
    canvas.create_oval(x, y, x+5, y+5, fill='black')
    message = f"{x},{y}"
    client_socket.send(message.encode())

# Bind canvas to mouse events
canvas.bind('<B1-Motion>', draw)

# Function to handle clear button click
def clear():
    canvas.delete('all')
    message = "clear"
    client_socket.send(message.encode())

# Create clear button widget
clear_button = tk.Button(window, text="Clear", command=clear)
clear_button.pack()

# Function to receive messages from server and update canvas
def receive():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message == "clear":
                canvas.delete('all')
            else:
                x, y = message.split(',')
                canvas.create_oval(int(x), int(y), int(x)+5, int(y)+5, fill='black')
        except:
            # Handle errors
            break

# Start thread to receive messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Start GUI loop
window.mainloop()
