import time, zenoh
from typing import Callable, Optional, Any

# A single Zenoh session for the entire process
_session: Optional[zenoh.Session] = None

def _get_session() -> zenoh.Session:
    """Initializes and returns a global Zenoh session."""
    global _session
    if _session is None:
        print("Opening Zenoh session...")
        conf = zenoh.Config()
        _session = zenoh.open(conf)
    return _session

class _Publisher:
    """Internal Publisher class using Zenoh."""
    def __init__(self, session: zenoh.Session, topic: str, msg_type: type) -> None:
        self.session = session
        self.key = topic
        self.msg_type = msg_type
        self.publisher = session.declare_publisher(topic)

    def publish(self, msg: Any) -> None:
        """Serializes and publishes a message."""
        assert isinstance(msg, self.msg_type), \
            f"Message type mismatch! Publisher for '{self.key}' expects '{self.msg_type.__name__}' but got '{type(msg).__name__}'"
        buf: bytes = msg.dumps()
        self.publisher.put(buf)

class _Subscriber:
    """Internal Subscriber class using Zenoh."""
    def __init__(self, session: zenoh.Session, topic: str, msg_type: type, callback: Callable[[Any], None]) -> None:
        self.session = session
        self.key = topic
        self.msg_type = msg_type
        self.user_callback = callback
        self.subscriber = session.declare_subscriber(topic, self._internal_callback)

    def _internal_callback(self, sample: zenoh.Sample) -> None:
        """Internal handler that receives raw data from Zenoh, deserializes it, and calls the user-defined callback."""
        try:
            msg = self.msg_type.loads(sample.payload.to_bytes())
            self.user_callback(msg)
        except Exception as e:
            print(f"Error deserializing message on topic '{self.key}': {e}")

class Node:
    """The main user-facing class for creating publishers and subscribers."""
    def __init__(self, node_name: str) -> None:
        self.name = node_name
        self.session = _get_session()

    def create_publisher(self, topic: str, msg_type: type) -> _Publisher:
        print(f"Node '{self.name}' creating publisher for topic '{topic}' with type '{msg_type.__name__}'.")
        return _Publisher(self.session, topic, msg_type)

    def create_subscriber(self, topic: str, msg_type: type, callback: Callable[[Any], None]) -> _Subscriber:
        print(f"Node '{self.name}' creating subscription for topic '{topic}' with type '{msg_type.__name__}'.")
        return _Subscriber(self.session, topic, msg_type, callback)
    
    def spin(self) -> None:
        try:
            print("Spinning to keep node alive...")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down node.")
            pass
