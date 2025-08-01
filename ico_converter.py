#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow가 필요합니다. `pip install pillow` 후 다시 실행하세요.", file=sys.stderr)
    sys.exit(1)

def load_image(path: Path, use_svg: bool):
    if path.suffix.lower() == ".svg":
        if not use_svg:
            raise ValueError("SVG를 직접 처리하려면 --svg 옵션을 켜거나, 먼저 PNG로 변환하세요.")
        try:
            import cairosvg
        except ImportError:
            raise ImportError("cairosvg가 필요합니다. `pip install cairosvg`")
        # cairosvg로 메모리에서 PNG 변환
        png_bytes = cairosvg.svg2png(url=str(path))
        from io import BytesIO
        return Image.open(BytesIO(png_bytes)).convert("RGBA")
    else:
        return Image.open(path).convert("RGBA")

def main():
    parser = argparse.ArgumentParser(
        description="PNG/SVG → 멀티 해상도 ICO 변환기 (Pillow 기반)"
    )
    parser.add_argument("input", type=Path, help="입력 이미지 (PNG, SVG 등)")
    parser.add_argument("-o", "--output", type=Path, default=None,
                        help="출력 ico 파일 경로 (기본: 입력파일명.ico)")
    parser.add_argument("-s", "--sizes", type=str, default="256,128,64,48,32,16",
                        help="쉼표로 구분된 정사각 해상도 목록 (예: 512,256,128,64,32,16)")
    parser.add_argument("--svg", action="store_true",
                        help="입력이 SVG일 때 cairosvg로 래스터라이즈")
    args = parser.parse_args()

    input_path = args.input
    if not input_path.exists():
        print(f"입력 파일이 존재하지 않습니다: {input_path}", file=sys.stderr)
        sys.exit(1)

    if args.output is None:
        args.output = input_path.with_suffix(".ico")

    # 해상도 파싱
    try:
        sizes = sorted({int(s.strip()) for s in args.sizes.split(",") if s.strip()})
    except ValueError:
        print("sizes 파싱 실패. 예: -s 256,128,64,48,32,16", file=sys.stderr)
        sys.exit(1)

    if any(s <= 0 for s in sizes):
        print("해상도는 양의 정수여야 합니다.", file=sys.stderr)
        sys.exit(1)

    # 이미지 로드
    try:
        img = load_image(input_path, use_svg=args.svg)
    except Exception as e:
        print(f"이미지 로드 실패: {e}", file=sys.stderr)
        sys.exit(1)

    # 가장 큰 사이즈보다 작은 원본이면 먼저 upscale 할지 여부는 취향인데,
    # 보통은 원본이 충분히 크도록(>= 512) 만들어주는 게 낫다.
    # 여기서는 Pillow가 알아서 리사이즈하므로 그대로 진행.
    resample = Image.Resampling.LANCZOS if hasattr(Image, "Resampling") else Image.LANCZOS

    # Pillow는 sizes=[(w,h), ...]만 넘겨주면 자체 리사이즈해서 ICO에 내장해준다.
    ico_sizes = [(s, s) for s in sizes]

    # 저장
    try:
        img.save(args.output, format="ICO", sizes=ico_sizes)
    except Exception as e:
        print(f"ICO 저장 실패: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"[+] Done: {args.output} (sizes={sizes})")

if __name__ == "__main__":
    main()

## 실행은 다음과 같이 하면 됨(터미널에 작성): python ico_converter.py icon.png (파일명이 icon.png여야함)