import logging

from simpleros import Node
from simpleros.msg.std_msg import String

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def timer_callback(publisher, i):
    msg = String(f"hello world {i[0]}")
    publisher.publish(msg)
    logger.info(f"TALKER SENDING: '{msg.data}'")
    i[0] += 1


def main():
    with Node("talker") as talker_node:
        publisher = talker_node.create_publisher("chatter", String)
        i = [0]  # in order to pass by reference
        talker_node.create_timer(1.0, timer_callback, publisher, i)
        talker_node.spin()


if __name__ == "__main__":
    main()
