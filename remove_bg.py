import sys
import os
import argparse
from pathlib import Path
from PIL import Image
from rembg import remove, new_session

def process_file(input_path: str, output_path: str = None, session = None):
    input_p = Path(input_path)
    if not input_p.is_file():
        print(f"Error: File not found: {input_path}")
        return False

    if output_path is None:
        output_p = input_p.with_name(f"{input_p.stem}_no_bg.png")
    else:
        output_p = Path(output_path)
        output_p.parent.mkdir(parents=True, exist_ok=True)

    print(f"Processing: {input_p.name} -> {output_p.name} ...")
    try:
        with Image.open(input_p) as img:
            result = remove(img.convert("RGBA"), session=session)
            result.save(output_p, "PNG")
        print(f"[OK] Saved to: {output_p}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Local Image Background Removal using rembg"
    )
    parser.add_argument("input", nargs="?", help="Input image file or directory")
    parser.add_argument("output", nargs="?", default=None, help="Output image file or directory (optional)")
    parser.add_argument("-m", "--model", default="u2net", help="Model name (default: u2net)")
    parser.add_argument("-b", "--batch", action="store_true", help="Batch mode: process all images in input folder")

    args = parser.parse_args()

    if not args.input:
        parser.print_help()
        sys.exit(1)

    session = new_session(args.model)
    in_path = Path(args.input)

    if args.batch or in_path.is_dir():
        out_dir = Path(args.output) if args.output else in_path / "output_no_bg"
        out_dir.mkdir(parents=True, exist_ok=True)
        extensions = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
        files = [p for p in in_path.iterdir() if p.suffix.lower() in extensions]
        print(f"Found {len(files)} images to process in {in_path}")
        for file in files:
            out_file = out_dir / f"{file.stem}_no_bg.png"
            process_file(str(file), str(out_file), session=session)
        print("Done!")
    else:
        process_file(str(in_path), args.output, session=session)

if __name__ == "__main__":
    main()
