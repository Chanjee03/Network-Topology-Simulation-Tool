import threading
import queue
import time

class NetworkNode(threading.Thread):
    def __init__(self, name, role, inbox):
        super().__init__()
        self.name = name
        self.role = role  # Router or Switch
        self.inbox = inbox
        self.running = True

    def run(self):
        while self.running:
            try:
                msg = self.inbox.get(timeout=1)
                print(f"[{self.name}] Received: {msg}")
                time.sleep(0.5)
            except:
                pass

    def stop(self):
        self.running = False

class NetworkSimulator:
    def __init__(self):
        self.nodes = {}
        self.links = {}

    def add_node(self, name, role):
        q = queue.Queue()
        node = NetworkNode(name, role, q)
        self.nodes[name] = node
        self.links[name] = q

    def start(self):
        for node in self.nodes.values():
            node.start()

    def send(self, src, dst, msg):
        if dst in self.links:
            self.links[dst].put(f"Packet from {src}: {msg}")

    def stop(self):
        for node in self.nodes.values():
            node.stop()
