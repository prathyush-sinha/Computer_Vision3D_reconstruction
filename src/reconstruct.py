"""SfM reconstruction and result parsing utilities."""

from __future__ import annotations

import re
from pathlib import Path

from src.config import ReconstructionConfig


STATS_PATTERNS = {
    "num_cameras": r"^\s*num_cameras\s*=\s*([0-9.]+)\s*$",
    "num_images": r"^\s*num_images\s*=\s*([0-9.]+)\s*$",
    "num_reg_images": r"^\s*num_reg_images\s*=\s*([0-9.]+)\s*$",
    "num_points3D": r"^\s*num_points3D\s*=\s*([0-9.]+)\s*$",
    "num_observations": r"^\s*num_observations\s*=\s*([0-9.]+)\s*$",
    "mean_track_length": r"^\s*mean_track_length\s*=\s*([0-9.]+)\s*$",
    "mean_observations_per_image": r"^\s*mean_observations_per_image\s*=\s*([0-9.]+)\s*$",
    "mean_reprojection_error": r"^\s*mean_reprojection_error\s*=\s*([0-9.]+)\s*$",
    "num_input_images": r"^\s*num_input_images\s*=\s*([0-9.]+)\s*$",
}


def run_sfm_reconstruction(config: ReconstructionConfig, image_list: list[str] | None = None):
    """Run COLMAP SfM through HLoc and return the reconstructed model object."""

    from hloc import reconstruction  # type: ignore
    from src.extract_features import list_images

    references = image_list or list_images(config.images)
    config.sfm_dir.mkdir(parents=True, exist_ok=True)

    return reconstruction.main(
        config.sfm_dir,
        config.images,
        config.sfm_pairs,
        config.features,
        config.matches,
        image_list=references,
    )


def parse_reconstruction_stats(text: str) -> dict[str, float | int]:
    """Parse COLMAP/HLoc reconstruction statistics from log text."""

    stats: dict[str, float | int] = {}
    for key, pattern in STATS_PATTERNS.items():
        match = re.search(pattern, text, flags=re.MULTILINE)
        if not match:
            continue

        value = float(match.group(1))
        stats[key] = int(value) if value.is_integer() else value

    return stats


def save_stats_markdown(stats: dict[str, float | int], output_path: str | Path) -> Path:
    """Save parsed reconstruction statistics as a small Markdown table."""

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    lines = ["# Reconstruction Statistics", "", "| Metric | Value |", "|---|---:|"]
    for key, value in stats.items():
        lines.append(f"| {key} | {value} |")

    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output
