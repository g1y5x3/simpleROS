# simpleROS

A lightweight, Python-first ROS alternative using Zenoh for messaging and Cap'n Proto for serialization.

## Why simpleROS
`simpleROS` is designed for developers and researchers who love the concepts of ROS (nodes, topics, publishers, subscribers) but want a simpler, more performant, and Python-native experience. By replacing the DDS middleware with **Zenoh** (which is also added in ROS 2) and the message system with **Cap'n Proto**, `simpleROS` offers several key advantages:
- High Performance: Leverages Zenoh's extremely low overhead and Cap'n Proto's zero-copy serialization for high-throughput, low-latency communication.
- Simplicity: A minimal, intuitive API that feels familiar to ROS 2 users but without the steep learning curve and build system complexity.
- Flexibility: Zenoh's ability to run in peer-to-peer or routed mode makes it suitable for everything from single-robot IPC to large-scale swarm communication.

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