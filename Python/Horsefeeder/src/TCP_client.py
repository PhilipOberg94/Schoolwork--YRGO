import socket
import time

# Pico's IP address (replace with the actual IP from the Pico's output)
PICO_IP = "192.168.4.3"  # Default range from Pi Zero AP; adjust as needed
PORT = 8024

def send_command(command):
    """Send a command to the Pico and return the response."""
    try:
        # Create a TCP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)  # Timeout after 5 seconds if no connection
        print(f"Attempting to connect to {PICO_IP}:{PORT}")
        
        # Connect to the Pico
        s.connect((PICO_IP, PORT))
        print("Connected to Pico")
        
        # Send the command
        s.send((command + "\r\n").encode())  # Add newline for consistency
        print(f"Sent command: {command}")
        
        # Receive response
        response = s.recv(1024).decode().strip()
        print("Response:", response)
        
        # Close the socket
        s.close()
        return response
    
    except ConnectionRefusedError:
        print("Connection refused. Is the Pico server running?")
    except socket.timeout:
        print("Connection timed out. Check IP and network.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    while True:  # This creates an infinite loop
        input_command = input("\nEnter a command, for example 'Group 3', Relay 3, Relay 4, or 'exit' to quit: ")
        
        if input_command.lower() == 'exit':  # Check if user wants to quit
            print("Exiting program...")
            break  # Exit the loop if 'exit' is entered
        
        response = send_command(input_command)
        # Optionally print the response if you want to show it
        print(response)
