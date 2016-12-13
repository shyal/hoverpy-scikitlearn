import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--capture",
    help="capture the data from hackernews",
    action="store_true")
parser.add_argument(
    "--verbose",
    help="print more information",
    action="store_true")
parser.add_argument(
    "--comments",
    help="include comments",
    action="store_true")
parser.add_argument(
    "--text",
    help="include post text",
    action="store_true")
args = parser.parse_args()
