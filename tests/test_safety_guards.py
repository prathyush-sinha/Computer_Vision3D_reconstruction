from pathlib import Path

import pytest

from scripts.run_reconstruction import refuse_dangerous_clean_path
from src.extract_features import list_images


def test_list_images_ignores_directories_with_image_suffix(tmp_path: Path):
    image_dir = tmp_path / "images"
    image_dir.mkdir()
    (image_dir / "frame001.jpg").write_bytes(b"fake image bytes")
    (image_dir / "frames.jpg").mkdir()

    assert list_images(image_dir) == ["frame001.jpg"]


def test_refuse_dangerous_clean_path_rejects_root():
    with pytest.raises(ValueError):
        refuse_dangerous_clean_path(Path("/"))


def test_refuse_dangerous_clean_path_rejects_home():
    with pytest.raises(ValueError):
        refuse_dangerous_clean_path(Path.home())
