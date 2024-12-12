import socket
import threading
from paramiko import Transport, ServerInterface, AUTH_FAILED, AUTH_SUCCESS

# Define the SSH Honeypot Server
class SSHHoneypot(ServerInterface):
    def __init__(self):
        # Initialize the authentication result
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        """
        Log the username and password attempts.
        This method is called when a client tries to authenticate with a username and password.
        """
        print(f"[LOGIN ATTEMPT] Username: {username}, Password: {password}")
        
        # Always fail the authentication to keep the honeypot active.
        return AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        """
        Handle channel requests from the client.
        This method can accept or reject channel requests.
        """
        print(f"[CHANNEL REQUEST] Type: {kind}, Channel ID: {chanid}")
        return AUTH_FAILED

# Function to handle an incoming SSH connection
def handle_connection(client_socket):
    """
    Handles an incoming SSH connection.
    Set up the Paramiko transport layer and bind it to the honeypot logic.
    """
    try:
        transport = Transport(client_socket)
        transport.add_server_key(paramiko.RSAKey.generate(2048))

        # Start the honeypot server
        honeypot = SSHHoneypot()
        transport.start_server(server=honeypot)

        # Keep the connection alive to simulate a real server
        channel = transport.accept()
        if channel:
            print("[SESSION] Client connected to fake shell.")
            channel.send(b"Welcome to the SSH Honeypot!\n")
            channel.close()
    except Exception as e:
        print(f"[ERROR] Connection handling failed: {e}")
    finally:
        client_socket.close()

# Main function to start the honeypot server
def start_honeypot(host='0.0.0.0', port=2222):
    """
    Starts the SSH honeypot server.
    Listens for incoming connections on the specified host and port.
    """
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(5)

        print(f"[HONEYPOT STARTED] Listening on {host}:{port}")

        while True:
            # Accept a new client connection
            client_socket, client_address = server_socket.accept()
            print(f"[NEW CONNECTION] {client_address}")

            # Handle the connection in a new thread
            threading.Thread(target=handle_connection, args=(client_socket,)).start()
    except Exception as e:
        print(f"[ERROR] Failed to start the honeypot: {e}")
    finally:
        server_socket.close()

# Run the honeypot server if executed as a script
if __name__ == "__main__":
    start_honeypot()
