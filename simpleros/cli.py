import argparse

import zenoh


def topic_list(conf: zenoh.Config):
    """Queries a Zenoh router to discover all known topics."""
    unique_topics = set()
    with zenoh.open(conf) as session:
        replies = session.liveliness().get("rt/**", timeout=5.0)
        for reply in replies:
            key_expr = str(reply.ok.key_expr)
            topic_name = key_expr.split("/")[2]
            unique_topics.add(topic_name)

    for topic in sorted(unique_topics):
        print(f"/{topic}")


def main():
    """
    The main entry point for the 'ros' command-line tool.
    """
    parser = argparse.ArgumentParser(
        prog="ros",
        description="A lightweight, ROS alternative using Capnp and Zenoh.",
    )
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Available commands"
    )

    # --- 'topic' command ---
    parser_topic = subparsers.add_parser("topic", help="Tools for inspecting topics.")
    topic_subparsers = parser_topic.add_subparsers(
        dest="topic_command", required=True, help="Topic commands"
    )
    parser_topic_list = topic_subparsers.add_parser(
        "list", help="List all active topics."
    )
    parser_topic_list.set_defaults(func=topic_list)

    args = parser.parse_args()

    conf = zenoh.Config()

    # Execute the function that was linked to the command
    if hasattr(args, "func"):
        args.func(conf)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
