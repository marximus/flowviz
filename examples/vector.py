from flowviz import animate
from flowviz import flowio

video = flowio.read_image_collection('../data/images')
flows = flowio.read_flow_collection('../data/flow')

flowanim = animate.FlowAnimation(video, vector=flows, vector_step=10, scale=0.5)
flowanim.save('output/vector.mp4')
