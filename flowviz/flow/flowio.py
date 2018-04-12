#  ".flo" file format used for optical flow evaluation
#
#  Stores 2-band float image for horizontal (u) and vertical (v) flow components.
#  Floats are stored in little-endian order.
#  A flow value is considered "unknown" if either |u| or |v| is greater than 1e9.
#
#   bytes  contents
#
#   0-3     tag: "PIEH" in ASCII, which in little endian happens to be the float 202021.25
#           (just a sanity check that floats are represented correctly)
#   4-7     width as an integer
#   8-11    height as an integer
#   12-end  data (width*height*2*4 bytes total)
#           the float values for u and v, interleaved, in row order, i.e.,
#           u[row0,col0], v[row0,col0], u[row0,col1], v[row0,col1], ...
#
TAG_FLOAT = 202021.25
TAG_STRING = "PIEH"

import re
import os

import numpy as np
import imageio


def read_flow(filename):
    """
    Read a .flo file.

    Parameters
    ----------
    filename : str
        Filename to read flow from. Must have extension .flo.

    Returns
    -------
    flow : ndarray, shape (height, width, 2)
        U and V vector components of flow.
    """
    ext = os.path.splitext(filename)[1]
    if ext != '.flo':
        quit('extension .flo expected')

    with open(filename, 'rb') as f:
        tag = np.fromfile(f, np.float32, count=1)[0]
        if tag != TAG_FLOAT:
            quit('invalid .flo file')
        width = np.fromfile(f, np.int32, 1)[0]
        height = np.fromfile(f, np.int32, 1)[0]

        data = np.fromfile(f, np.float32, count=2*width*height)
        flow = np.resize(data, (height, width, 2))

    return flow


def write_flow(filename, flow):
    """
    Write a .flo file.

    Parameters
    ----------
    filename : str
        Filename where flow will be saved. Must have extension .flo.
    flow : ndarray, shape (height, width, 2), dtype float32
        Flow to save to file.

    Returns
    -------
    None
    """
    ext = os.path.splitext(filename)[1]
    if ext != '.flo':
        quit('extension .flo expected')
    if not (flow.ndim == 3 and flow.shape[-1] == 2):
        quit('flow must have shape (height, width, 2)')
    if flow.dtype != np.float32:
        quit('flow must have dtype float32')

    height, width, _ = flow.shape

    with open(filename, 'wb') as f:
        tag = np.array([TAG_FLOAT], dtype=np.float32)
        width = np.array([width], dtype=np.int32)
        height = np.array([height], dtype=np.int32)

        tag.tofile(f)
        width.tofile(f)
        height.tofile(f)
        flow.tofile(f)


def read_flow_collection(dirname):
    """
    Load a collection of .flo files.

    An example directory may look like:

        dirname
            - frame_0001.flo
            - frame_0002.flo
            - ...

    Parameters
    ----------
    dirname : str
        Directory containing .flo files.

    Returns
    -------
    flows : ndarray, shape (N, H, W, 2)
        Sequence of flow components.
    """
    pattern = re.compile("\d+")

    files = []

    allfiles = [f for f in os.listdir(dirname) if f.endswith('.flo')]
    for f in allfiles:
        match = pattern.findall(f)
        if len(match) == 1:
            frame_index = int(match[0])
            filepath = os.path.join(dirname, f)
            files.append((frame_index, filepath))
    files = sorted(files, key=lambda x: x[0])

    flows = []
    for frame_index, filepath in files:
        flow_frame = read_flow(filepath)
        flows.append(flow_frame)

    flows = np.array(flows)

    return flows


def read_image_collection(dirname, format='.png'):
    """
    Load a collection of images.

    Parameters
    ----------
    dirname : str
        Directory containing image files.
    format : str, optional
        Extension of images to load.

    Returns
    -------
    images : ndarray, shape (N, H, W) or (N, H, W, 3) or (N, H, W, 4)
        Sequence of images.
    """
    image_files = []

    files = [f for f in os.listdir(dirname) if f.endswith(format)]
    for f in files:
        match = re.findall('\d+', f)
        if len(match) == 1:
            frame_index = int(match[0])
            filepath = os.path.join(dirname, f)
            image_files.append((frame_index, filepath))
    image_files = sorted(image_files, key=lambda x: x[0])

    images = [imageio.imread(f) for _, f in image_files]
    images = np.array(images)

    return images

