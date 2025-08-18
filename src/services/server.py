from flask import Flask
from threading import Thread
from src.config.config import config

class KeepAliveServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def home():
            return "Auto Scrobbler is running!"

    def run(self):
        """Run the Flask server."""
        self.app.run(
            host=config.server['host'],
            port=config.server['port']
        )

    def start_server(self):
        """Start the server in a separate thread."""
        server_thread = Thread(target=self.run)
        server_thread.daemon = True  # Set as daemon so it stops when the main program stops
        server_thread.start()
        return server_thread

def create_server():
    """Factory function to create and start the server."""
    server = KeepAliveServer()
    return server.start_server()