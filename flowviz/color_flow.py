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
def motion_to_color(motim, maxmotion=None, verbose=False):
    """

    Parameters
    ----------
    motim : ndarray, dtype float, shape (height, width, 2)
        Motion image of vectors.
    maxmotion :

    Returns
    -------
    colim : ndarray, dtype uint8, shape (height, width, 3)
        Colored image.
    """
    height, width, _ = motim.shape
    colim = np.zeros((height, width, 3), dtype=np.uint8)

    # determine motion range
    maxx, maxy = motim[:, :, 0].max(), motim[:, :, 1].max()
    minx, miny = motim[:, :, 0].min(), motim[:, :, 1].min()
    fx = motim[:, :, 0]
    fy = motim[:, :, 1]
    rad = np.sqrt(fx**2 + fy**2)
    maxrad = rad.max()
    print("max motion: {:.4f}   motion range: u = {:.3f} .. {:.3f};  v = {:.3f} .. {:.3f}".format(
        maxrad, minx, maxx, miny, maxy
    ))

    if maxmotion is not None:
        maxrad = maxmotion

    if maxrad == 0:
        maxrad = 1

    if verbose:
        print("normalizing by {}".format(maxrad))

    colorcode.compute_color(fx/maxrad, fy/maxrad, colim)

    idx = _unknown_flow(fx, fy)
    colim[idx] = 0

    return colim


def main(flowname, maxmotion=None):
    flow = np.load(flowname)
    flow = np.moveaxis(flow, 0, -1)
    im = flow[0]

    outim = motion_to_color(im, maxmotion)

    # save to file
    from matplotlib.image import imsave
    imsave('color-flow.png', outim, dpi=100)


