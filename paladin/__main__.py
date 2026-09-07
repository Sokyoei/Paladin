import argparse


def parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=9131, type=int, help="port")
    parser.add_argument('-a', '--address', default="127.0.0.1", type=str, help="ip address")
    return parser.parse_args()


def main() -> None:
    args = parser()
    print(args)


if __name__ == '__main__':
    main()
