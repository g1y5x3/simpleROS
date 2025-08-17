# simpleROS

A lightweight, Python-first ROS alternative using Zenoh for messaging and Cap'n Proto 
for serialization.

## Why simpleROS
simpleROS is a faster and easier version of ROS for Python developers. It keeps the 
familiar ROS concepts (nodes, topics, etc.) but swaps out the underlying technology for 
two modern tools: [Zenoh](https://github.com/eclipse-zenoh/zenoh) and 
[Cap'n Proto](https://github.com/capnproto/capnproto).

This results in three main benefits:

🚀 **High Performance**

Leverages Zenoh's extremely low overhead and Cap'n Proto's zero-copy serialization for high-throughput, low-latency communication.

😊 **Simplicity**

A minimal, intuitive API that feels familiar to ROS 2 users but without the steep learning curve and build system complexity.

🤸 **Flexibility**: 

Zenoh's ability to run in peer-to-peer or routed mode makes it suitable for everything from single-robot IPC to large-scale swarm communication.

## Installation

### 1. System Dependencies (Cap'n Proto Compiler)

First, you need the `capnp` command-line tool to compile message schemas.

**On Debian/Ubuntu:**

```bash
sudo apt-get update && sudo apt-get install capnproto
```
### 2. Install simpleROS from Source
```
# Clone the repository
git clone https://github.com/g1y5x3/simpleROS.git
cd simpleROS

# Install the library in editable mode
# This also compiles the .capnp message files automatically
pip install -e .

# To install development tools like 'ruff', use the [dev] extra:
pip install -e .[dev]
```

### To-DO
- [ ] Implement `ros node`-like command-line interface.
- [ ] Implement `ros topic`-like command-line interface.

### Notes
1. About the trade-off of supporting features like *[ros2 topic list](https://discord.com/channels/914168414178779197/940584045287460885/1161275196880203836)* 