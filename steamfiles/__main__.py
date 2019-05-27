from argparse import ArgumentParser
from pprint import PrettyPrinter

from . import acf, appinfo, manifest

parser = ArgumentParser(
    prog="steamfiles",
    description=" Python library for parsing the most common Steam file formats. ",
)
parser.add_argument(
    "type", choices=["acf", "appinfo", "manifest"], help="the type of file"
)
parser.add_argument("file", type=str, help="file to parse")
args = parser.parse_args()

if args.type == "acf":
    mode = "r"
    module = acf
if args.type == "appinfo":
    mode = "rb"
    module = appinfo
if args.type == "manifest":
    mode = "rb"
    module = manifest

pp = PrettyPrinter()
with open(args.file, mode) as f:
    data = module.load(f)
    pp.pprint(data)
