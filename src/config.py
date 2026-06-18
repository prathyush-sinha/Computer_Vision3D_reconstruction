"""Configuration utilities for the 3D reconstruction pipeline.

The functions in this file avoid importing HLoc directly so basic tests can run
without a full COLMAP/HLoc installation.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


SUPPORTED_FEATURE_CONFIGS = {
    "sift",
    "superpoint_max",
    "superpoint_aachen",
    "disk",
}

SUPPORTED_MATCHER_CONFIGS = {
    "adalam",
    "superpoint+lightglue",
    "superpoint+superglue",
    "disk+lightglue",
}


@dataclass(frozen=True)
class ReconstructionConfig:
    """Resolved paths and algorithm choices for a reconstruction run."""

    images: Path
    outputs: Path
    feature_conf: str = "sift"
    matcher_conf: str = "adalam"

    @property
    def sfm_pairs(self) -> Path:
        return self.outputs / "pairs-sfm.txt"

    @property
    def sfm_dir(self) -> Path:
        return self.outputs / "sfm"

    @property
    def features(self) -> Path:
        return self.outputs / "features.h5"

    @property
    def matches(self) -> Path:
        return self.outputs / "matches.h5"

    @property
    def database(self) -> Path:
        return self.outputs / "database.db"


def validate_images_path(images: Path) -> None:
    """Validate that an image directory exists and contains image-like files."""

    if not images.exists():
        raise FileNotFoundError(f"Image directory does not exist: {images}")

    if not images.is_dir():
        raise NotADirectoryError(f"Expected an image directory: {images}")

    image_suffixes = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp"}
    if not any(path.suffix.lower() in image_suffixes for path in images.iterdir()):
        raise ValueError(f"No image files found in: {images}")


def build_config(
    images: str | Path,
    outputs: str | Path,
    feature_conf: str = "sift",
    matcher_conf: str = "adalam",
    validate_paths: bool = True,
) -> ReconstructionConfig:
    """Create and validate a reconstruction config."""

    images_path = Path(images).expanduser().resolve()
    outputs_path = Path(outputs).expanduser().resolve()

    if feature_conf not in SUPPORTED_FEATURE_CONFIGS:
        raise ValueError(
            f"Unsupported feature_conf={feature_conf!r}. "
            f"Choose from {sorted(SUPPORTED_FEATURE_CONFIGS)}."
        )

    if matcher_conf not in SUPPORTED_MATCHER_CONFIGS:
        raise ValueError(
            f"Unsupported matcher_conf={matcher_conf!r}. "
            f"Choose from {sorted(SUPPORTED_MATCHER_CONFIGS)}."
        )

    if validate_paths:
        validate_images_path(images_path)

    return ReconstructionConfig(
        images=images_path,
        outputs=outputs_path,
        feature_conf=feature_conf,
        matcher_conf=matcher_conf,
    )
