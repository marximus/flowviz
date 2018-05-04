[![Build Status](https://travis-ci.com/marximus/flowviz.svg?branch=master)](https://travis-ci.com/marximus/flowviz)

# Flowviz
Flowviz is a Python animation library based on matplotlib that provides a high-level interface for visualizing flow. 

## Installation
#### Conda
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

## Usage
For more examples, check out the Jupyter [notebook](https://nbviewer.jupyter.org/github/marximus/flowviz/blob/master/notebooks/examples.ipynb).
```python
import flowviz
import flowviz.flow.flowio as flowio

video = flowio.read_image_collection('sample_data/images')
anim = flowviz.FlowAnimation(video)
anim.save('flow-animation.mp4')
```

## Acknowledgments
Code for coloring flow was adapted from the [Middlebury optical flow dataset](http://vision.middlebury.edu/flow).

## License
MIT License
