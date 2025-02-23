import cowsay
import argparse


parser = argparse.ArgumentParser(description="Display two cows with their messages.")
parser.add_argument("-f", "--cow1", default="default", help="Cowfile for the first cow")
parser.add_argument("message1", nargs='?', default="Gamarjoba!", help="Message for the first cow")
parser.add_argument("-E", "--eyes2", default="oo", help="Eyes for the second cow")
parser.add_argument(
    "-F", "--cow2", default="default", help="Cowfile for the second cow"
)
parser.add_argument("-N", "--tongue2", default="  ", help="Tongue for the second cow")
parser.add_argument("message2", nargs='?', default="Gamarjoba!", help="Message for the second cow")
args = parser.parse_args()
cows = cowsay.list_cows()
if args.cow1 in cows and args.cow2 in cows:
    cow1_lines = cowsay.cowsay(message=args.message1, cow=args.cow1).split("\n")
    cow2_lines = cowsay.cowsay(
        message=args.message2, cow=args.cow2, eyes=args.eyes2, tongue=args.tongue2
    ).split("\n")

    max_len = max(len(cow1_lines), len(cow2_lines))
    cow1_lines = [""] * (max_len - len(cow1_lines)) + cow1_lines
    cow2_lines = [""] * (max_len - len(cow2_lines)) + cow2_lines
    width = max(len(line) for line in cow1_lines)
    combined = []
    for line1, line2 in zip(cow1_lines, cow2_lines):
        combined.append(line1.ljust(width) + line2)
    print("\n".join(combined))
