from flowviz import animate, colorflow, flowio

video = flowio.read_image_collection('../data/images')
flows = flowio.read_flow_collection('../data/flow')

colors = colorflow.motion_to_color(flows)
flowanim = animate.FlowAnimation(video=video, video2=colors, vector=flows, vector_step=10, video2_alpha=0.5, scale=0.5)
flowanim.save('output/vector_color.mp4')