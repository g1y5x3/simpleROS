import zenoh
import time
from typing import Callable, Optional, Any

# A single Zenoh session for the entire process
_session: Optional[zenoh.Session] = None

def get_session() -> zenoh.Session:
    """Initializes and returns a global Zenoh session."""
    global _session
    if _session is None:
        print("Opening Zenoh session...")
        _session = zenoh.open()
    return _session

class _Publisher:
    """Internal Publisher class using Zenoh."""
    def __init__(self, session: zenoh.Session, topic: str, msg_type: type) -> None:
        self.session = session
        self.key = topic
        self.msg_type = msg_type

    def publish(self, data: Any) -> None:
        """Serializes data dynamically based on the provided message type and publishes it with Zenoh."""
        payload: bytes = self.msg_type.to_bytes_packed(data)
        self.session.put(self.key, payload)

class _Subscriber:
    """Internal Subscriber class using Zenoh."""
    def __init__(self, session: zenoh.Session, topic: str, msg_type: type, callback: Callable[[Any], None]) -> None:
        self.msg_type = msg_type
        def zenoh_listener(sample: zenoh.Sample):
            msg = self.msg_type.from_bytes_packed(sample.payload)
            callback(msg)
        self.subscriber = session.declare_subscriber(topic, zenoh_listener)

class Node:
    """The main user-facing class for creating publishers and subscribers."""
    def __init__(self, node_name: str) -> None:
        self.name = node_name
        self.session = get_session()
        print(f"Node '{self.name}' initialized with Zenoh.")

    def create_publisher(self, topic: str, msg_type: type) -> _Publisher:
        print(f"Node '{self.name}' creating publisher for topic '{topic}' with type '{msg_type.__name__}'.")
        return _Publisher(self.session, topic, msg_type)

    def create_subscriber(self, topic: str, msg_type: type, callback: Callable[[Any], None]) -> _Subscriber:
        print(f"Node '{self.name}' creating subscription for topic '{topic}' with type '{msg_type.__name__}'.")
        return _Subscriber(self.session, topic, msg_type, callback)

def spin() -> None:
    """Keeps the main program alive to allow Zenoh's background tasks to run."""
    print("Spinning to keep node alive...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")