import pytest

from src.config import build_config


def test_rejects_unknown_feature_config(tmp_path):
    with pytest.raises(ValueError, match="Unsupported feature_conf"):
        build_config(
            tmp_path,
            tmp_path / "outputs",
            feature_conf="unknown-extractor",
            validate_paths=False,
        )


def test_rejects_unknown_matcher_config(tmp_path):
    with pytest.raises(ValueError, match="Unsupported matcher_conf"):
        build_config(
            tmp_path,
            tmp_path / "outputs",
            matcher_conf="unknown-matcher",
            validate_paths=False,
        )


def test_supports_superpoint_lightglue_pair(tmp_path):
    cfg = build_config(
        tmp_path,
        tmp_path / "outputs",
        feature_conf="superpoint_max",
        matcher_conf="superpoint+lightglue",
        validate_paths=False,
    )

    assert cfg.feature_conf == "superpoint_max"
    assert cfg.matcher_conf == "superpoint+lightglue"
