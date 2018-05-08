from flowviz import animate, flowio, colorflow


video = flowio.read_image_collection('../data/images')
flows = flowio.read_flow_collection('../data/flow')

colors = colorflow.motion_to_color(flows)
flowanim = animate.FlowAnimation(colors, scale=0.5)
flowanim.save('output/color.mp4')
