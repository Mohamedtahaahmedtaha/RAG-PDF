import argparse
import json
from .api import extract_pdf_api

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_path", help="Path to PDF file")
    parser.add_argument("-o", "--output", help="Output JSON file", default="output.json")
    args = parser.parse_args()

    result = extract_pdf_api(args.pdf_path)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    print(f"✅ Extraction completed: {args.output}")

if __name__ == "__main__":
    main()
