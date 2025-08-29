import argparse
from . import greet

def main() -> None:
    parser = argparse.ArgumentParser(description="Nova sample CLI")
    parser.add_argument("--name", help="Name to greet")
    args = parser.parse_args()
    if args.name:
        print(f"Hello, {args.name}!")
    else:
        greet()

if __name__ == "__main__":
    main()
