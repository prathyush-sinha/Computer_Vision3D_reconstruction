"""Command-line entrypoint for the modular reconstruction pipeline."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from src.config import build_config
from src.extract_features import extract_local_features, list_images
from src.match_features import match_local_features
from src.reconstruct import run_sfm_reconstruction


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run HLoc/COLMAP 3D reconstruction.")
    parser.add_argument("--images", required=True, help="Directory containing input images.")
    parser.add_argument("--outputs", default="outputs/demo-front", help="Output directory.")
    parser.add_argument("--feature-conf", default="sift", help="HLoc feature config.")
    parser.add_argument("--matcher-conf", default="adalam", help="HLoc matcher config.")
    parser.add_argument("--clean", action="store_true", help="Remove output directory before running.")
    return parser.parse_args()


def refuse_dangerous_clean_path(path: Path) -> None:
    """Refuse cleanup targets that are filesystem roots or home directories."""

    resolved = path.expanduser().resolve()
    home = Path.home().resolve()

    if resolved == resolved.anchor or resolved == home:
        raise ValueError(f"Refusing to delete unsafe output path: {resolved}")

    if len(resolved.parts) <= 2:
        raise ValueError(f"Refusing to delete broad output path: {resolved}")


def main() -> None:
    args = parse_args()
    config = build_config(
        images=args.images,
        outputs=args.outputs,
        feature_conf=args.feature_conf,
        matcher_conf=args.matcher_conf,
    )

    if args.clean and config.outputs.exists():
        refuse_dangerous_clean_path(config.outputs)
        shutil.rmtree(config.outputs)

    config.outputs.mkdir(parents=True, exist_ok=True)
    image_list = list_images(config.images)
    print(f"Found {len(image_list)} input images.")

    print("Extracting local features...")
    extract_local_features(config, image_list=image_list)

    print("Matching local features...")
    match_local_features(config, image_list=image_list)

    print("Running SfM reconstruction...")
    model = run_sfm_reconstruction(config, image_list=image_list)

    print("Reconstruction complete.")
    print(model)


if __name__ == "__main__":
    main()
