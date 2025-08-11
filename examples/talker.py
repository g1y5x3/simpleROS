from simpleros import Node
from simpleros.msg.std_msg import String

msg = String(data="Hello, Simple ROS!")
message = msg.dumps()
msg2 = String.loads(message)
print(f'Received message: {msg2.data}')