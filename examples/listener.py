from simpleros import Node
from simpleros.msg.std_msg import String


def listener_callback(msg: String):
    print(f"LISTENER RECEIVED: '{msg.data}'")


def main():
    with Node("listener") as listener_node:
        listener_node.create_subscriber("chatter", String, listener_callback)
        listener_node.spin()  # Blocks execution to process callbacks


if __name__ == "__main__":
    main()
