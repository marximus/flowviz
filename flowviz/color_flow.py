import numpy as np

import flowviz.colorcode as colorcode


"""
flowIO.h
"""
UNKNOWN_FLOW_THRESH = 1e9


"""
flowIO.cpp
"""
def unknown_flow(u, v):
    """

    Parameters
    ----------
    u : float
    v : float

    Returns
    -------
    bool
    """
    return (np.fabs(u) > UNKNOWN_FLOW_THRESH) | (np.fabs(v) > UNKNOWN_FLOW_THRESH) | np.isnan(u) | np.isnan(v)


"""
color_flow.cpp
"""
def MotionToColor(motim, maxmotion=None, verbose=False):
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
    sh = motim.shape
    width, height = sh[1], sh[0]
    colim = np.zeros((height, width, 3), dtype=np.uint8)

    # determine motion range
    maxx, maxy = motim[:, :, 0].max(), motim[:, :, 1].max()
    minx, miny = motim[:, :, 0].min(), motim[:, :, 1].min()
    fx = motim[:, :, 0]
    fy = motim[:, :, 1]
    rad = np.sqrt(fx * fx + fy * fy)
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

    for y in range(0, height):
        for x in range(0, width):
            fx = motim[y, x, 0]
            fy = motim[y, x, 1]
            pix = colim[y, x]
            if unknown_flow(fx, fy):
                pix[0] = pix[1] = pix[2] = 0
            else:
                colorcode.computeColor(fx/maxrad, fy/maxrad, pix)

    return colim


def main(flowname, outname, maxmotion=None):
    flow = np.load(flowname)
    flow = np.moveaxis(flow, 0, -1)
    im = flow[0]
    # sh = (im.shape[0], im.shape[1], 3)
    # outim = np.zeros(sh, dtype=np.uint8)
    outim = MotionToColor(im, maxmotion)

    # save to file
    from matplotlib.image import imsave
    imsave(outname, outim, dpi=100)


