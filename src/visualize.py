"""Helpers for documenting reconstruction output artifacts."""

from __future__ import annotations

from pathlib import Path


def ensure_output_notes(output_dir: str | Path) -> Path:
    """Create a README file inside an output directory."""

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    note = output / "README.md"
    note.write_text(
        "# Output Artifacts\n\n"
        "Store reconstruction result figures and exported geometry files here after rerunning the pipeline.\n",
        encoding="utf-8",
    )
    return note
