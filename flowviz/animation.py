import numpy as np
import matplotlib.animation as animation
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure


class FlowAnimation:
    """
    Class for flow animations.

    Parameters
    ----------
    video : ndarray, shape (N, H, W)
        Sequence of images.
    vector : ndarray, shape (2, N, H, W), optional
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
    imshow_kws : dict, optional
        Keyword arguments passed to `Axes.imshow`.
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
    def __init__(self, video, vector=None, vector_step=1, scale=1.0, dpi=100, imshow_kws=None, quiver_kws=None):
        # TODO: Allow NxHxWx3 and NxHxWx4 video arrays
        if video.ndim != 3:
            quit('video must have 3 dimensions')
        if vector is not None:
            if vector.ndim != 4:
                quit('vector must have 4 dimensions')
            if vector.shape[0] != 2:
                quit('shape of first vector dimension must be 2')
            if vector.shape[1:] != video.shape:
                quit('shape of last three dimensions of video and vector must match')

        # set up keyword arguments
        imshow_kws = {} if imshow_kws is None else imshow_kws.copy()
        imshow_kws.update(dict(animated=True, aspect='equal', cmap='gray', vmin=0, vmax=255))
        quiver_kws = {} if quiver_kws is None else quiver_kws.copy()
        quiver_kws.update(dict(angles='xy', scale_units='xy', scale=1, pivot='tail'))

        N, H, W = video.shape
        figsize = (np.array((W, H)) * scale).astype(np.int)

        fig = Figure(figsize=figsize/dpi, dpi=dpi, frameon=False)
        FigureCanvasAgg(fig)
        ax = fig.add_axes((0, 0, 1, 1))
        ax.axis('off')

        im = ax.imshow(np.zeros((H, W), dtype=video.dtype), **imshow_kws)

        if vector is None:
            UV = None
            quiver = None
        else:
            X, Y = np.meshgrid(np.arange(W), np.arange(H))
            X, Y = X[::vector_step, ::vector_step], Y[::vector_step, ::vector_step]
            UV = vector[:, :, ::vector_step, ::vector_step]

            quiver = ax.quiver(X, Y, np.zeros((H, W), dtype=UV.dtype), np.zeros((H, W), dtype=UV.dtype), **quiver_kws)

        self.fig = fig
        self.ax = ax
        self.im = im
        self.quiver = quiver
        self.N = N
        self.figwidth, self.figheight = figsize

        self._video = video
        self._UV = UV
        self._dpi = dpi

    def _draw_frame(self, idx):
        self.im.set_data(self._video[idx])
        if self._UV is not None:
            self.quiver.set_UVC(self._UV[0, idx], self._UV[1, idx])

    def save(self, filename, fps=5, bitrate=-1, codec=None):
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

        Returns
        -------
        None
        """
        # TODO: Should user be able to use other writers such as FFMpegFileWriter?
        writer = animation.FFMpegWriter(fps=fps, bitrate=bitrate, codec=codec)
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
