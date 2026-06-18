"""Feature matching helpers built around Hierarchical Localization (HLoc)."""

from __future__ import annotations

from src.config import ReconstructionConfig
from src.extract_features import list_images


def get_hloc_matcher_config(name: str):
    """Resolve an HLoc matcher configuration by name."""

    from hloc import match_features  # type: ignore

    try:
        return match_features.confs[name]
    except KeyError as exc:
        available = ", ".join(sorted(match_features.confs))
        raise KeyError(f"Unknown HLoc matcher config {name!r}. Available: {available}") from exc


def match_local_features(config: ReconstructionConfig, image_list: list[str] | None = None) -> Path:
    """Generate exhaustive pairs and match local features."""

    from hloc import match_features, pairs_from_exhaustive  # type: ignore

    config.outputs.mkdir(parents=True, exist_ok=True)
    references = image_list or list_images(config.images)
    matcher_conf = get_hloc_matcher_config(config.matcher_conf)

    pairs_from_exhaustive.main(config.sfm_pairs, image_list=references)
    match_features.main(
        matcher_conf,
        config.sfm_pairs,
        features=config.features,
        matches=config.matches,
    )
    return config.matches
