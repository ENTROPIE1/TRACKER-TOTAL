import argparse
from .db import Database


def cmd_start(args):
    db = Database()
    session_id = db.start_session(args.telegram_id)
    print(f"Started session {session_id} for user {args.telegram_id}")


def cmd_message(args):
    db = Database()
    db.store_message(args.session_id, args.telegram_id, args.text)
    print("Message stored")


def cmd_end(args):
    db = Database()
    summary = db.end_session(args.session_id)
    print(f"Session {args.session_id} ended. Summary:\n{summary}")


def cmd_latest(args):
    db = Database()
    summary = db.latest_session_summary(args.telegram_id)
    if summary:
        print(f"Latest summary for {args.telegram_id}: {summary}")
    else:
        print("No summary found")


def main():
    parser = argparse.ArgumentParser(description="Tracker CLI")
    sub = parser.add_subparsers()

    p_start = sub.add_parser("start_session")
    p_start.add_argument("telegram_id", type=int)
    p_start.set_defaults(func=cmd_start)

    p_msg = sub.add_parser("message")
    p_msg.add_argument("session_id", type=int)
    p_msg.add_argument("telegram_id", type=int)
    p_msg.add_argument("text")
    p_msg.set_defaults(func=cmd_message)

    p_end = sub.add_parser("end_session")
    p_end.add_argument("session_id", type=int)
    p_end.set_defaults(func=cmd_end)

    p_latest = sub.add_parser("latest_summary")
    p_latest.add_argument("telegram_id", type=int)
    p_latest.set_defaults(func=cmd_latest)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
