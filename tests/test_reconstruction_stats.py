from pathlib import Path

from src.reconstruct import parse_reconstruction_stats, save_stats_markdown


SAMPLE_LOG = """
Reconstruction:
    num_cameras = 1
    num_images = 27
    num_reg_images = 27
    num_points3D = 2432
    num_observations = 8308
    mean_track_length = 3.41612
    mean_observations_per_image = 307.704
    mean_reprojection_error = 1.25835
    num_input_images = 104
"""


def test_parse_reconstruction_stats():
    stats = parse_reconstruction_stats(SAMPLE_LOG)

    assert stats["num_input_images"] == 104
    assert stats["num_reg_images"] == 27
    assert stats["num_points3D"] == 2432
    assert stats["mean_reprojection_error"] == 1.25835


def test_save_stats_markdown(tmp_path: Path):
    output = save_stats_markdown(
        {"num_input_images": 104, "mean_reprojection_error": 1.25835},
        tmp_path / "stats.md",
    )

    text = output.read_text(encoding="utf-8")
    assert "| num_input_images | 104 |" in text
    assert "| mean_reprojection_error | 1.25835 |" in text
