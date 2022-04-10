import itertools as it
import numpy as np
import os

def get_coords(index, pear_corner, pomegranate_corner, natural_cost,
		actor_action, step_size):
	# Set the ordering of the fruits (counterclockwise from the decider).
	if pear_corner == coords[index]["fruit"][0]:
		first_fruit = pear_corner
		second_fruit = pomegranate_corner
	else:
		first_fruit = pomegranate_corner
		second_fruit = pear_corner

	# If the decider starts off on the bottom-left corner.
	if index == 0:
		# Update the fruit coordinates.
		first_fruit -= np.array([8.0-natural_cost[0]*step_size, 0.0])
		second_fruit -= np.array([0.0, 8.0-natural_cost[1]*step_size])

		# The actor either does nothing, raises the cost of the first
		# fruit, or raises the cost of the second fruit.
		if sum(actor_action) == 0:
			boulder_coords = None
		elif np.argmax(actor_action) == 0:
			first_boulder = [first_fruit[0]-step_size, first_fruit[1]]
			boulder_coords = [first_boulder]
			for action in range(1, actor_action[0]):
				more_boulders = np.array([
					first_boulder[0],
					first_boulder[1]+(step_size*action)
				])
				boulder_coords.append(more_boulders)
		else:
			first_boulder = [second_fruit[0], second_fruit[1]-step_size]
			boulder_coordinates = [first_boulder]
			for action in range(1, actor_action[1]):
				more_boulders = np.array([
					first_boulder[0]+(step_size*action),
					first_boulder[1]
				])
				boulder_coordinates.append(more_boulders)

	# If the decider starts off on the bottom-right corner.
	elif index == 1:
		# Update the fruit coordinates.
		first_fruit -= np.array([0.0, 8.0-natural_cost[0]*step_size])
		second_fruit += np.array([8.0-natural_cost[1]*step_size, 0.0])

		# The actor either does nothing, raises the cost of the first
		# fruit, or raises the cost of the second fruit.
		if sum(actor_action) == 0:
			boulder_coords = None
		elif np.argmax(actor_action) == 0:
			first_boulder = [first_fruit[0], first_fruit[1]-step_size]
			boulder_coords = [first_boulder]
			for action in range(1, actor_action[0]):
				more_boulders = np.array([
					first_boulder[0]-(step_size*action),
					first_boulder[1]
				])
				boulder_coords.append(more_boulders)
		else:
			first_boulder = [second_fruit[0]+step_size, second_fruit[1]]
			boulder_coords = [first_boulder]
			for action in range(1, actor_action[1]):
				more_boulders = np.array([
					first_boulder[0],
					first_boulder[1]+(step_size*action)
				])
				boulder_coords.append(more_boulders)

	# If the decider starts off on the top-right corner.
	elif index == 2:
		# Update the fruit coordinates.
		first_fruit += np.array([8.0-natural_cost[0]*step_size, 0.0])
		second_fruit += np.array([0.0, 8.0-natural_cost[1]*step_size])

		# The actor either does nothing, raises the cost of the first
		# fruit, or raises the cost of the second fruit.
		if sum(actor_action) == 0:
			boulder_coords = None
		elif np.argmax(actor_action) == 0:
			first_boulder = [first_fruit[0]+step_size, first_fruit[1]]
			boulder_coords = [first_boulder]
			for action in range(1, actor_action[0]):
				more_boulders = np.array([
					first_boulder[0],
					first_boulder[1]-(step_size*action)
				])
				boulder_coords.append(more_boulders)
		else:
			first_boulder = [second_fruit[0], second_fruit[1]+step_size]
			boulder_coords = [first_boulder]
			for action in range(1, actor_action[1]):
				more_boulders = np.array([
					first_boulder[0]-(step_size*action),
					first_boulder[1]
				])
				boulder_coords.append(more_boulders)

	# If the decider starts off on the top-left corner.
	else:
		# Update the fruit coordinates.
		first_fruit += np.array([0.0, 8.0-natural_cost[0]*step_size])
		second_fruit -= np.array([8.0-natural_cost[1]*step_size, 0.0])

		# The actor either does nothing, raises the cost of the first
		# fruit, or raises the cost of the second fruit.
		if sum(actor_action) == 0:
			boulder_coords = None
		elif np.argmax(actor_action) == 0:
			first_boulder = [first_fruit[0], first_fruit[1]+step_size]
			boulder_coords = [first_boulder]
			for action in range(1, actor_action[0]):
				more_boulders = np.array([
					first_boulder[0]+(step_size*action),
					first_boulder[1]
				])
				boulder_coords.append(more_boulders)
		else:
			first_boulder = [second_fruit[0]-step_size, second_fruit[1]]
			boulder_coord  = [first_boulder]
			for action in range(1, actor_action[1]):
				more_boulders = np.array([
					first_boulder[0],
					first_boulder[1]-(step_size*action)
				])
				boulder_coords.append(more_boulders)

	if pear_corner == coords[index]["fruit"][0]:
		return first_fruit, second_fruit, boulder_coords
	else:
		return second_fruit, first_fruit, boulder_coords

if __name__ == "__main__":
	# Set up how the stimuli will be varied.
	coords = {
		0: {"decider": [0.5, 0.5], "fruit": [[9.5, 0.5], [0.5, 9.5]]},
		1: {"decider": [9.5, 0.5], "fruit": [[9.5, 9.5], [0.5, 0.5]]},
		2: {"decider": [9.5, 9.5], "fruit": [[0.5, 9.5], [9.5, 0.5]]},
		3: {"decider": [0.5, 9.5], "fruit": [[0.5, 0.5], [9.5, 9.5]]},
	}
	natural_costs = np.array(list(it.product([5, 7, 9], repeat=2)))
	actor_actions = np.array([[0, 0], [1, 0], [2, 0], [3, 0]])
	step_size = 1.0

	# Create the stimuli by iterating through all potential combinations of 
	# decider and fruit positions, creating a tex file, converting it to a pdf
	# file, then converting that to a png file, and then finally renaming it.
	for index in coords:
		if index == 0 or index == 1:
			continue
		decider_coords = coords[index]["decider"]
		grass = "grass_" + str(index)
		fruit_corners = coords[index]["fruit"]
		for pear_corner in fruit_corners:
			pomegranate_corner = [pomegranate_corner for pomegranate_corner \
				in fruit_corners if pomegranate_corner != pear_corner][0]
			path = str(np.array(decider_coords)) + "/" \
				+ str(np.array(pear_corner)) + "/"
			for natural_cost in natural_costs:
				for actor_action in actor_actions:
					filename = str(natural_cost) + "_" + str(actor_action)
					pear_coords, pomegranate_coords, boulder_coords = \
						get_coords(index, pear_corner, pomegranate_corner,
							natural_cost, actor_action, step_size)
					with open(path+filename+".tex", "w", newline="") as file:
						file.write("\\documentclass{standalone}\n\n" + \
								   "\\usepackage{tikz}\n" + \
								   "\\usepackage{graphicx}\n" + \
								   "\\graphicspath{{C:/Data/Research/physical_pragmatics/stimuli/observer_0/}}\n\n" + \
								   "\\begin{document}\n" + \
								   "\\begin{tikzpicture}\n")
						file.write("\\node[anchor=south west,inner sep=0] at (0,0) {\\includegraphics{%s}};\n" % \
							(grass))
						file.write("\\begin{scope}[shift={(0.39, 0.39)}]\n" + \
								   "\\draw[step=1.0cm,color=black, fill=white] (0,0) grid (10,10) rectangle (0,0);\n")
						file.write("\\node at (%f,%f) {\\includegraphics[scale=0.17]{hiker}};\n" % \
							(decider_coords[0], decider_coords[1]))
						file.write("\\node at (%f,%f) {\\includegraphics[scale=0.0175]{pear}};\n" % \
							(pear_coords[0]-0.25, pear_coords[1]-0.25))
						file.write("\\node at (%f,%f) {\\includegraphics[scale=0.0175]{pear}};\n" % \
							(pear_coords[0]+0.25, pear_coords[1]-0.25))
						file.write("\\node at (%f,%f) {\\includegraphics[scale=0.0175]{pear}};\n" % \
							(pear_coords[0]+0.25, pear_coords[1]+0.25))
						file.write("\\node at (%f,%f) {\\includegraphics[scale=0.0175]{pear}};\n" % \
							(pear_coords[0]-0.25, pear_coords[1]+0.25))
						file.write("\\node at (%f,%f) {\\includegraphics[scale=0.0175]{pomegranate}};\n" % \
							(pomegranate_coords[0]-0.25, pomegranate_coords[1]-0.25))
						file.write("\\node at (%f,%f) {\\includegraphics[scale=0.0175]{pomegranate}};\n" % \
							(pomegranate_coords[0]+0.25, pomegranate_coords[1]-0.25))
						file.write("\\node at (%f,%f) {\\includegraphics[scale=0.0175]{pomegranate}};\n" % \
							(pomegranate_coords[0]+0.25, pomegranate_coords[1]+0.25))
						file.write("\\node at (%f,%f) {\\includegraphics[scale=0.0175]{pomegranate}};\n" % \
							(pomegranate_coords[0]-0.25, pomegranate_coords[1]+0.25))
						if sum(actor_action) != 0:
							for action in range(max(actor_action)):
								if len(np.shape(boulder_coords)) == 1:
									file.write("\\node at (%f,%f) {\\includegraphics[scale=0.45]{boulder}};\n" % \
										(boulder_coords[0], boulder_coords[1]))
								else:
									file.write("\\node at (%f,%f) {\\includegraphics[scale=0.45]{boulder}};\n" % \
										(boulder_coords[action][0], boulder_coords[action][1]))
						file.write("\\end{scope}\n" + \
								   "\\end{tikzpicture}\n" + \
								   "\\end{document}\n")
					os.system("pdflatex " + "\"" + path + filename + ".tex\"")
					os.system("pdftoppm -r 500 -png \"" + filename + ".pdf\" \"" + path + filename + "\"")
					os.chdir(path)
					os.system("rename " + "\"" + filename + "-1.png\"" + " \"" + filename + ".png\"")
					os.chdir("../../")
