import sys
import numpy as np


ncols = 0
MAXCOLS = 60
colorwheel = np.empty((MAXCOLS, 3))


def setcols(r, g, b, k):
    global colorwheel

    colorwheel[k, 0] = r
    colorwheel[k, 1] = g
    colorwheel[k, 2] = b


def makecolorwheel():
    global ncols

    RY = 15
    YG = 6
    GC = 4
    CB = 11
    BM = 13
    MR = 6
    ncols = RY + YG + GC + CB + BM + MR
    if ncols > MAXCOLS:
        sys.exit(1)

    k = 0
    for i in range(0, RY):
        setcols(255, 255*i/RY, 0, k)
        k += 1
    for i in range(0, YG):
        setcols(255-255*i/YG, 255, 0, k)
        k += 1
    for i in range(0, GC):
        setcols(0, 255, 255*i/GC, k)
        k += 1
    for i in range(0, CB):
        setcols(0, 255-255*i/CB, 255, k)
        k += 1
    for i in range(0, BM):
        setcols(255*i/BM, 0, 255, k)
        k += 1
    for i in range(0, MR):
        setcols(255, 0, 255-255*i/MR, k)
        k += 1


def computeColor(fx, fy, pix):
    """

    Parameters
    ----------
    fx : float
    fy : float
    pix : ndarray view, dtype uint8, shape(3,)

    Returns
    -------
    None
    """
    if ncols == 0:
        makecolorwheel()

    rad = np.sqrt(fx * fx + fy * fy)
    a = np.arctan2(-fy, -fx) / np.pi
    fk = (a + 1.0) / 2.0 * (ncols - 1)
    k0 = int(fk)
    k1 = (k0 + 1) % ncols
    f = fk - k0
    # f = 0  // uncomment to see original color wheel
    for b in range(0, 3):
        col0 = colorwheel[k0][b] / 255.0
        col1 = colorwheel[k1][b] / 255.0
        col = (1 - f) * col0 + f * col1
        if rad <= 1:
            col = 1 - rad * (1 - col)  # increase saturation with radius
        else:
            col *= .75  # out of range
        pix[2 - b] = int(255.0 * col)
