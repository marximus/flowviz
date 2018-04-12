import tempfile
import os

import numpy as np
import matplotlib.animation as animation
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure


class FlowAnimation:
    """
    Class for flow animations.

    Parameters
    ----------
    video : ndarray, shape (N, H, W) or (N, H, W, 3) or (N, H, W, 4)
        Sequence of images.
    video2 : ndarray, shape (N, H, W) or (N, H, W, 3) or (N, H, W, 4)
        Sequence of images.
    vector : ndarray, shape (N, H, W, 2), optional
        An array containing the u (vector[0]) and v (vector[1]) components of vectors. Vectors will be drawn
        at equally spaced points on the grid from (x, y) to (x+u, y+v).
    vector_step : int, optional
        Only plot every `vector_step` arrow.
    scale : float, optional
        Scale size of output. If scale == 1 (default) the output size will be W x H, where W and H are the width
        and height of `video` and
    dpi : int, optional
        Dots per inch passed to Figure. Does not actually change outputs of save() or to_rgba() but is included
        to support features in the future.
    video2_alpha : float, optional
        Value of alpha passed to Axes.imshow for video2.
    imshow_kws_1 : dict, optional
        Keyword arguments passed to `Axes.imshow` for video.
    imshow_kws_2 : dict, optional
        Keyword arguments passed to `Axes.imshow` for video2.
    quiver_kws : dict, optional
        Keyword arguments passed to `Axes.quiver`.

    Attributes
    ----------
    fig : matplotlib Figure
        Figure object used to draw animation frames.
    ax : matplotlib Axes
        Axes object in figure.
    im : matplotlib.image.AxesImage
        Image displayed on axis.
    quiver : matplotlib Quiver
        Quiver object used to display vectors on axis.
    figwidth : int
        Width of output (in pixels)
    figheight : int
        Height of output (in pixels)
    """
    def __init__(self, video, video2=None, vector=None, vector_step=1, scale=1.0, dpi=100,
                 video2_alpha=0.5, imshow_kws_1=None, imshow_kws_2=None, quiver_kws=None):
        if not (video.ndim == 3 or video.ndim == 4):
            quit('video must have 3 or 4 dimensions')
        if video.ndim == 4 and not (video.shape[-1] == 3 or video.shape[-1] == 4):
            quit('video must be NxHxWx3 or NxHxWx4')
        if video2 is not None:
            if not (video2.ndim == 3 or video2.ndim == 4):
                quit('video2 must have 3 or 4 dimensions')
            if video2.ndim == 4 and not (video2.shape[-1] == 3 or video2.shape[-1] == 4):
                quit('video2 must be NxHxWx3 or NxHxWx4')
        if vector is not None:
            if vector.ndim != 4:
                quit('vector must have 4 dimensions')
            if vector.shape[-1] != 2:
                quit('shape of last vector dimension must be 2')
            if vector.shape[:3] != video.shape[:3]:
                quit('video and vector must have same length, height, and width')

        # set up keyword arguments
        imshow_kws_1 = {} if imshow_kws_1 is None else imshow_kws_1.copy()
        imshow_kws_1.update(dict(animated=True, aspect='equal', interpolation='none'))
        imshow_kws_2 = {} if imshow_kws_2 is None else imshow_kws_2.copy()
        imshow_kws_2.update(dict(animated=True, aspect='equal', interpolation='none', alpha=video2_alpha))
        quiver_kws = {} if quiver_kws is None else quiver_kws.copy()
        quiver_kws.update(dict(angles='xy', scale_units='xy', scale=1, pivot='tail'))

        # if video is NxHxW use greyscale colormapping
        if video.ndim == 3:
            imshow_kws_1.update(dict(cmap='gray', vmin=0, vmax=255))
        if video2 is not None and video2.ndim == 3:
            imshow_kws_2.update(dict(cmap='gray', vmin=0, vmax=255))

        N, H, W = video.shape[:3]
        figsize = (np.array((W, H)) * scale).astype(np.int)

        fig = Figure(figsize=figsize/dpi, dpi=dpi, frameon=False)
        FigureCanvasAgg(fig)
        ax = fig.add_axes((0, 0, 1, 1))
        ax.axis('off')

        im = ax.imshow(np.zeros_like(video[0]), **imshow_kws_1)
        if video2 is None:
            im2 = None
        else:
            # TODO: Rather than using alpha, create new array of video2 with alpha channel where the transparency
            # is set based on the magnitude of pixel values.
            im2 = ax.imshow(np.zeros_like(video2[0]), **imshow_kws_2)

        if vector is None:
            UV = None
            quiver = None
        else:
            X, Y = np.meshgrid(np.arange(W), np.arange(H))
            X, Y = X[::vector_step, ::vector_step], Y[::vector_step, ::vector_step]
            UV = vector[:, ::vector_step, ::vector_step, :]

            quiver = ax.quiver(X, Y, np.zeros((H, W), dtype=UV.dtype), np.zeros((H, W), dtype=UV.dtype), **quiver_kws)

        self.fig = fig
        self.ax = ax
        self.im = im
        self.im2 = im2
        self.quiver = quiver
        self.N = N
        self.figwidth, self.figheight = figsize

        self._video = video
        self._video2 = video2
        self._UV = UV
        self._dpi = dpi

    def _draw_frame(self, idx):
        self.im.set_data(self._video[idx])
        if self._video2 is not None:
            self.im2.set_data(self._video2[idx])
        if self._UV is not None:
            self.quiver.set_UVC(self._UV[idx, :, :, 0], self._UV[idx, :, :, 1])

    def save(self, filename, fps=5, bitrate=-1, codec=None, writer='pipe'):
        """
        Save movie file by drawing every frame.

        Parameters
        ----------
        filename : str
            Output filename.
        fps : int
            Frames per second of movie.
        bitrate : int
            Number of bits used per second in the compressed movie, in kilobits per second.
        codec : string or None, optional
            The codec to use. If ``None`` (the default) the ``animation.codec`` rcParam is used.
        writer : {'pipe', 'file'}
            Determines if a file-based (FFMpegFileWriter) or pipe-based (FFMpegWriter) writer will be used. The
            file-based writer makes use of the specified dpi and can produce nicer videos. The pipe-based writer
            is quicker.

        Returns
        -------
        None
        """
        if not (writer == 'file' or writer == 'pipe'):
            quit('writer must be file or pipe')

        writer = animation.FFMpegWriter if writer == 'pipe' else animation.FFMpegFileWriter

        writer = writer(fps=fps, bitrate=bitrate, codec=codec)
        with writer.saving(self.fig, filename, self._dpi):
            for i in range(self.N):
                self._draw_frame(i)
                writer.grab_frame()

    def to_rgba(self):
        """
        Return animation as array of RGBA images.

        Returns
        -------
        rgba : ndarray, shape (N, H, W, 4)
            An array of N RGBA images with height H and width W.
        """
        rgba = np.empty((self.N, self.figheight, self.figwidth, 4), dtype=np.uint8)
        for i in range(self.N):
            self._draw_frame(i)
            self.fig.canvas.draw()
            rgba[i] = np.array(self.fig.canvas.renderer._renderer)

        return rgba

    def to_jshtml(self, fps=5, loop=True, embed_limit=20):
        """
        Generate HTML representation of the animation.

        Parameters
        ----------
        fps : int
            Frames per second of movie.
        loop : bool
            Whether the video should loop or not.
        embed_limit : int, optional
            Limit, in MB, of size of encoded animation in HTML.

        Returns
        -------
        html : str
            HTML representation of video.
        """
        default_mode = 'loop' if loop else 'once'

        writer = animation.HTMLWriter(fps=fps, embed_frames=True, default_mode=default_mode, embed_limit=embed_limit)

        # Can't open a second time while opened on windows. So we avoid
        # deleting when closed, and delete manually later.
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
            with writer.saving(self.fig, f.name, self._dpi):
                for i in range(self.N):
                    self._draw_frame(i)
                    writer.grab_frame()

        with open(f.name) as fobj:
            html = fobj.read()

        os.remove(f.name)

        return html
