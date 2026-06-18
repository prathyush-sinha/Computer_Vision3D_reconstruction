# Reconstruction Statistics

These statistics are preserved from the original exploratory notebook run.

| Metric | Value |
|---|---:|
| Input images | 104 |
| Registered images | 27 |
| Sparse 3D points | 2,432 |
| Observations | 8,308 |
| Mean track length | 3.41612 |
| Mean observations per image | 307.704 |
| Mean reprojection error | 1.25835 px |

## Interpretation

Only 27 of 104 input images were registered in the largest model. This is usable evidence that the pipeline ran end-to-end, but it also shows the capture setup had limited reconstruction coverage.

Likely reasons:

- many images were captured from one dominant side of the scene;
- limited parallax between views;
- some views may have had weak texture or insufficient overlap;
- exhaustive matching produced many pairs, but geometric verification and SfM kept only a subset.

## Suggested next run

For a stronger portfolio result, rerun the pipeline with a more complete circular/arc capture path and export:

- sparse reconstruction screenshot;
- dense point cloud or mesh;
- `.ply` point cloud;
- before/after comparison of SIFT+AdaLAM vs SuperPoint+LightGlue.
