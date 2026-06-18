from pathlib import Path

import pytest

from src.config import build_config, validate_images_path


def test_build_config_without_path_validation(tmp_path: Path):
    cfg = build_config(
        images=tmp_path / "images",
        outputs=tmp_path / "outputs",
        feature_conf="sift",
        matcher_conf="adalam",
        validate_paths=False,
    )

    assert cfg.feature_conf == "sift"
    assert cfg.matcher_conf == "adalam"
    assert cfg.sfm_pairs.name == "pairs-sfm.txt"
    assert cfg.features.name == "features.h5"
    assert cfg.matches.name == "matches.h5"


def test_validate_images_path_requires_existing_directory(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        validate_images_path(tmp_path / "missing")


def test_validate_images_path_requires_images(tmp_path: Path):
    empty_dir = tmp_path / "images"
    empty_dir.mkdir()

    with pytest.raises(ValueError):
        validate_images_path(empty_dir)


def test_validate_images_path_accepts_image_files(tmp_path: Path):
    image_dir = tmp_path / "images"
    image_dir.mkdir()
    (image_dir / "frame001.jpg").write_bytes(b"fake image bytes")

    validate_images_path(image_dir)
