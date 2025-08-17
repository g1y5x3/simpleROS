import logging

from simpleros import Node
from simpleros.msg.std_msg import String

logging.basicConfig(level=logging.DEBUG)


def main():
    with Node("talker") as talker_node:
        talker_node.create_publisher("chatter", String)

        def timer_callback(counter):
            msg = String(f"hello world {counter[0]}")
            talker_node.publish("chatter", msg)
            print(f"TALKER SENDING: '{msg.data}'")
            counter[0] += 1

        i = [0]  # in order to pass by reference
        talker_node.create_timer(1.0, timer_callback, i)
        talker_node.spin()


if __name__ == "__main__":
    main()
