"""Feature extraction helpers built around Hierarchical Localization (HLoc)."""

from __future__ import annotations

from pathlib import Path

from src.config import ReconstructionConfig


def list_images(images: Path) -> list[str]:
    """Return image file names relative to the image directory."""

    suffixes = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp"}
    return sorted(
        path.relative_to(images).as_posix()
        for path in images.iterdir()
        if path.suffix.lower() in suffixes
    )


def get_hloc_feature_config(name: str):
    """Resolve an HLoc feature configuration by name.

    HLoc is imported lazily so unit tests can validate repo code without a full
    HLoc/COLMAP environment.
    """

    from hloc import extract_features  # type: ignore

    try:
        return extract_features.confs[name]
    except KeyError as exc:
        available = ", ".join(sorted(extract_features.confs))
        raise KeyError(f"Unknown HLoc feature config {name!r}. Available: {available}") from exc


def extract_local_features(config: ReconstructionConfig, image_list: list[str] | None = None) -> Path:
    """Run local feature extraction and return the feature file path."""

    from hloc import extract_features  # type: ignore

    config.outputs.mkdir(parents=True, exist_ok=True)
    references = image_list or list_images(config.images)
    feature_conf = get_hloc_feature_config(config.feature_conf)

    extract_features.main(
        feature_conf,
        config.images,
        image_list=references,
        feature_path=config.features,
    )
    return config.features
