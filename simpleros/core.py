import logging
import threading
import time
from typing import Any, Callable, List, Optional, Type

import zenoh

# A single Zenoh session for the entire process
_session: Optional[zenoh.Session] = None


def _get_session() -> zenoh.Session:
    """Initializes and returns a global Zenoh session."""
    global _session
    if _session is None:
        conf = zenoh.Config()
        _session = zenoh.open(conf)
    return _session


def _shutdown_session() -> None:
    """Closes the global Zenoh session."""
    global _session
    if _session is not None:
        _session.close()
        _session = None


def get_msg_type_string(msg_type: Type) -> str:
    """Returns a string representation of the message type."""
    return f"{msg_type.__module__.split('.')[2]}/{msg_type.__name__}"


class _Publisher:
    """Internal Publisher class using Zenoh."""

    def __init__(
        self, node_name: str, session: zenoh.Session, topic: str, msg_type: type
    ) -> None:
        self.logger = logging.getLogger(f"{node_name}.publisher(/{topic})")
        self.session = session
        self.msg_type = msg_type

        self.key = f"rt/{topic}"
        self.token_key = f"{self.key}/pub:{get_msg_type_string(msg_type)}"
        self.logger.debug(f"data key: {self.key}")
        self.logger.debug(f"token key: {self.token_key}")

        self.publisher = session.declare_publisher(self.key)
        self.token = session.liveliness().declare_token(self.token_key)

    def publish(self, msg: Any) -> None:
        """Serializes and publishes a message."""
        assert isinstance(msg, self.msg_type)
        buf: bytes = msg.dumps()
        self.publisher.put(buf)


class _Subscriber:
    """Internal Subscriber class using Zenoh."""

    def __init__(
        self,
        node_name: str,
        session: zenoh.Session,
        topic: str,
        msg_type: type,
        callback: Callable[[Any], None],
    ) -> None:
        self.logger = logging.getLogger(f"{node_name}.subscriber(/{topic})")
        self.session = session
        self.msg_type = msg_type

        self.key = f"rt/{topic}"
        self.token_key = f"{self.key}/sub:{get_msg_type_string(msg_type)}"
        self.logger.debug(f"data key: {self.key}")
        self.logger.debug(f"token key: {self.token_key}")

        self.subscriber = session.declare_subscriber(self.key, self._internal_callback)
        self.user_callback = callback

    def _internal_callback(self, sample: zenoh.Sample) -> None:
        """Internal handler that receives Zbytes from Zenoh and deserializes it."""
        msg = self.msg_type.loads(sample.payload.to_bytes())
        self.user_callback(msg)


class _RepeatingTimer(threading.Thread):
    """A timer thread that calls a function at regular intervals."""

    def __init__(
        self, interval: float, function: Callable, args=None, kwargs=None
    ) -> None:
        super().__init__()
        self.interval = interval
        self.function = function
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self.stop_event = threading.Event()
        self.daemon = True  # Allow thread

    def run(self) -> None:
        """The main loop of the timer thread."""
        while not self.stop_event.wait(self.interval):
            self.function(*self.args, **self.kwargs)

    def stop(self) -> None:
        """Stops the timer thread."""
        self.stop_event.set()


class Node:
    """The main user-facing class for creating publishers and subscribers."""

    def __init__(self, node_name: str) -> None:
        self.logger = logging.getLogger(f"{node_name}")
        self.node_name = node_name
        self._timers: List[_RepeatingTimer] = []

        self.logger.debug(f"Creating node '{self.node_name}'...")
        self.session = _get_session()

    def __enter__(self) -> "Node":
        return self

    def __exit__(self, exc_type, exc_value, exec_tb) -> None:
        self.shutdown()

    def create_publisher(self, topic: str, msg_type: type) -> _Publisher:
        self.logger.debug(
            f"Node '{self.node_name}' creating publisher for topic '{topic}' with "
            f"type '{msg_type.__name__}'."
        )
        return _Publisher(self.node_name, self.session, topic, msg_type)

    def create_subscriber(
        self, topic: str, msg_type: type, callback: Callable[[Any], None]
    ) -> _Subscriber:
        self.logger.debug(
            f"Node '{self.node_name}' creating subscription for topic '{topic}' with "
            f"type '{msg_type.__name__}'."
        )
        return _Subscriber(self.node_name, self.session, topic, msg_type, callback)

    def create_timer(
        self, period_sec: float, callback: Callable, *args, **kwargs
    ) -> None:
        timer = _RepeatingTimer(period_sec, callback, args=args, kwargs=kwargs)
        self._timers.append(timer)
        timer.start()

    def spin(self) -> None:
        """Blocks execution to process callbacks until a KeyboardInterrupt (Ctrl+C)."""
        try:
            while True:
                time.sleep(1)  # Sleep to prevent high CPU usage
        except KeyboardInterrupt:
            self.logger.info("\nReceiving keyboard interrupt...")

    def shutdown(self) -> None:
        """Shuts down the node and closes the Zenoh session."""
        self.logger.debug(f"Shutting down node '{self.node_name}'...")
        for timer in self._timers:
            timer.stop()
        _shutdown_session()
