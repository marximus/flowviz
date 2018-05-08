# Flowviz
Flowviz is a Python animation library based on matplotlib that provides a high-level interface for visualizing flow. 

## Installation
#### Conda
[![Build Status](https://travis-ci.com/marximus/flowviz.svg?branch=master)](https://travis-ci.com/marximus/flowviz)

With [conda](https://conda.io/docs/index.html) installed, run
```
conda install -c conda-forge -c mauricemarx flowviz
```
#### Source
If you plan to edit the code, you can install manually.
```
git clone https://github.com/marximus/flowviz
cd flowviz
pip install -e .
```

## Examples
Check out the Jupyter [notebook](https://nbviewer.jupyter.org/github/marximus/flowviz/blob/master/notebooks/examples.ipynb).

#### Vectors
![](examples/output/vector.gif)
#### Colors
![](examples/output/color.gif)
#### Vectors and Colors
![](examples/output/vector_color.gif)

## Acknowledgments
Code for coloring flow was adapted from the [Middlebury optical flow dataset](http://vision.middlebury.edu/flow).

## License
MIT License
