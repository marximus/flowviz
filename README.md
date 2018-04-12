# Flowviz

## Installation
#### Conda
> conda install -c mauricemarx flowviz

## Usage
For more examples, check out the Jupyter [notebook](notebooks/examples.ipynb).
```python
import flowviz
import flowviz.flow.flowio as flowio

video = flowio.read_image_collection('sample_data/images')
anim = flowviz.FlowAnimation(video)
anim.save('flow-animation.mp4')
```

## Credits

## License