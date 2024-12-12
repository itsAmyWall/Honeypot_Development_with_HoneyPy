# SSH Honeypot

## Overview
The SSH Honeypot is a Python-based application designed to simulate an SSH server. It captures and logs unauthorized login attempts to analyze potential security threats. 

## Features
- **Simulated SSH Server**: Mimics an SSH server to attract attackers.
- **Login Attempt Logging**: Logs all username and password attempts for analysis.
- **Fake Shell Session**: Provides a basic interaction to make it appear like a real SSH service.
- **Configurable**: You can change the listening IP and port.

## Installation

### Prerequisites
- Python 3.7 or higher
- `paramiko` library

### Install Dependencies
Use `pip` to install the required dependencies:
```bash
pip install paramiko
```

## Usage

### Starting the Honeypot
Run the following command to start the honeypot server:
```bash
python ssh_honeypot.py
```
By default, the honeypot listens on `0.0.0.0` (all interfaces) and port `2222`.

### Redirect SSH Traffic
To redirect SSH traffic (port 22) to the honeypot port (2222), you can use `iptables` on Linux:
```bash
sudo iptables -t nat -A PREROUTING -p tcp --dport 22 -j REDIRECT --to-port 2222
```

### Logs
All login attempts are logged in the terminal output, including:
- Username
- Password
- Channel requests

### Example Output
```plaintext
[HONEYPOT STARTED] Listening on 0.0.0.0:2222
[NEW CONNECTION] ('192.168.1.100', 52345)
[LOGIN ATTEMPT] Username: admin, Password: password123
[LOGIN ATTEMPT] Username: root, Password: toor
[SESSION] Client connected to fake shell.
```

## Code Breakdown

### Main Components
1. **SSHHoneypot Class**: Implements the SSH server interface to log authentication attempts and handle channel requests.
2. **handle_connection Function**: Manages individual client connections using the Paramiko `Transport`.
3. **start_honeypot Function**: Sets up the server socket to listen for incoming SSH connections.

## Security Notice
This SSH honeypot is for **educational purposes only**
## Future Enhancements
- Add IP banning for repeated attempts.
- Log data to a file or database for better analysis.
- Simulate additional SSH features to increase believability.


## Acknowledgements
- Built using the `paramiko` library for SSH protocol handling.

## Contributing
Feel free to submit pull requests or issues to improve the project!
