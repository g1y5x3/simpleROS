from simpleros import Node
from simpleros.msg.std_msg import String


def timer_callback(publisher, i):
    msg = String(f"hello world {i[0]}")
    publisher.publish(msg)
    print(f"TALKER SENDING: '{msg.data}'")
    i[0] += 1


def main():
    with Node("talker") as talker_node:
        publisher = talker_node.create_publisher("chatter", String)
        i = [0]  # in order to pass by reference instead of value
        talker_node.create_timer(1.0, timer_callback, publisher, i)
        talker_node.spin()


if __name__ == "__main__":
    main()
