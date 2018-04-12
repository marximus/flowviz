import numpy as np

import flowviz.colorcode as colorcode


"""
flowIO.h
"""
UNKNOWN_FLOW_THRESH = 1e9


"""
flowIO.cpp
"""
def _unknown_flow(u, v):
    return (np.fabs(u) > UNKNOWN_FLOW_THRESH) | (np.fabs(v) > UNKNOWN_FLOW_THRESH) | np.isnan(u) | np.isnan(v)


"""
color_flow.cpp
"""
def motion_to_color(inmotim, maxmotion=None, verbose=False):
    """

    Parameters
    ----------
    inmotim : ndarray, dtype float, shape (height, width, 2) OR (length, height, width, 2)
        Array of vector components. Can be either a single array or a sequence of arrays of vector components.
    maxmotion : float
        Maximum value to normalize by.

    Returns
    -------
    colim : ndarray, shape (height, width, 3) or (length, height, width, 3), dtype uint8
        Colored image.
    """
    if inmotim.ndim == 3:
        motim = inmotim[None, ...]
    else:
        motim = inmotim

    if motim.ndim != 4 or motim.shape[-1] != 2:
        quit('motim must be a (length, height, width, 2) array')

    length, height, width, _ = motim.shape
    colim = np.zeros((length, height, width, 3), dtype=np.uint8)

    # determine motion range
    # maxx, maxy = motim[..., 0].max(), motim[..., 1].max()
    # minx, miny = motim[..., 0].min(), motim[..., 1].min()
    fx = motim[:, :, :, 0]
    fy = motim[:, :, :, 1]
    rad = np.sqrt(fx**2 + fy**2)
    maxrad = rad.max()
    # print("max motion: {:.4f}   motion range: u = {:.3f} .. {:.3f};  v = {:.3f} .. {:.3f}".format(
    #     maxrad, minx, maxx, miny, maxy
    # ))

    if maxmotion is not None:
        maxrad = maxmotion

    if maxrad == 0:
        maxrad = 1

    if verbose:
        print("normalizing by {}".format(maxrad))

    for i in range(length):
        fx = motim[i, :, :, 0]
        fy = motim[i, :, :, 1]
        colorcode.compute_color(fx/maxrad, fy/maxrad, colim[i])

    fx = motim[:, :, :, 0]
    fy = motim[:, :, :, 1]
    idx = _unknown_flow(fx, fy)
    colim[idx] = 0

    if inmotim.ndim == 3:
        return colim[0]
    return colim
