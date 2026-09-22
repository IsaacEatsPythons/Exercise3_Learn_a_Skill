import argparse
import json
from pathlib import Path

from src.pipeline import parse_datasheet

#function to allow main to run from command line
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser( description="Extract selectable text from PDF datasheet." )
    parser.add_argument("pdf_path", type=Path)

    return parser


def main() -> None:
    args = build_parser().parse_args() 
    extracted_fields = parse_datasheet(args.pdf_path)
    json_output = json.dumps(extracted_fields, indent=2)

    print(f"Parsing: {args.pdf_path.name}")
    print(json_output)

    output_path = Path("output") / f"{args.pdf_path.stem}.json"
    output_path.write_text(json_output)

    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
