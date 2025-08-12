import time
from simpleros import Node
from simpleros.msg.std_msg import String


def main():
    talker_node = Node("talker")
    publisher = talker_node.create_publisher("chatter", String)
    i = 0

    try:
        while True:
            msg = String(f"hello world {i}")
            publisher.publish(msg)
            print(f"TALKER SENDING: '{msg.data}'")
            i += 1
            time.sleep(1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
