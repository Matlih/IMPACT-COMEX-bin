import argparse

from src.app import app


def parse_args():
    parser = argparse.ArgumentParser(description="Run the OpenCV sorting app.")
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without opening the OpenCV preview window.",
    )
    parser.add_argument(
        "--no-headless",
        action="store_true",
        help="Force preview window on, overriding config headless mode.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.headless and args.no_headless:
        raise ValueError("Use only one of --headless or --no-headless.")

    headless = None
    if args.headless:
        headless = True
    elif args.no_headless:
        headless = False

    app(headless=headless)

if __name__ == "__main__":
    main()
