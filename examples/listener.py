import time
from simpleros import Node
from simpleros.msg.std_msg import String


def listener_callback(msg: String):
    print(f"LISTENER RECEIVED: '{msg.data}'")


def main():
    listener_node = Node("listener")
    listener_node.create_subscriber("chatter", String, listener_callback)

    try:
        while True:
            time.sleep(0.1)  # Keep the listener alive to receive messages
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
