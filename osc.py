from pythonosc import dispatcher
from pythonosc import osc_server


def handle_all_messages(address, *args):
    print(f"Received message: {address} {args}")
# Create a dispatcher
osc_dispatcher = dispatcher.Dispatcher()
osc_dispatcher.set_default_handler(handle_all_messages)  # Catch all messages

# Define the server address and port
ip = "10.106.50.72"  # Localhost
port = 8002

# Create and start the server
server = osc_server.ThreadingOSCUDPServer((ip, port), osc_dispatcher)
print(f"Serving on {server.server_address}")

try:
    server.serve_forever()  # Keep the server running
except KeyboardInterrupt:
    print("\nServer stopped")
