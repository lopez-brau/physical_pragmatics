import itertools as it
import numpy as np
import os

def get_coords(index, pear_corner, pomegranate_corner, natural_cost, enforcer_action, step_size):
	# Set the ordering of the fruits (counterclockwise from the agent).
	if pear_corner == coords[index]["fruit"][0]:
		first_fruit = pear_corner
		second_fruit = pomegranate_corner
	else: 
		first_fruit = pomegranate_corner
		second_fruit = pear_corner

	# If the agent starts off on the bottom-left corner.
	if index == 0:
		# Update the fruit coordinates.
		first_fruit -= np.array([6.0-natural_cost[0]*step_size, 0.0])
		second_fruit -= np.array([0.0, 6.0-natural_cost[1]*step_size])

		# The enforcer either does nothing, raises the cost of the first
		# fruit, or raises the cost of the second fruit.
		if sum(enforcer_action) == 0:
			boulder_coords = None
		elif np.argmax(enforcer_action) == 0:
			first_boulder = [first_fruit[0]-step_size, first_fruit[1]]
			boulder_coords = [first_boulder]
			for action in range(1, enforcer_action[0]):
				if action == 2:
					more_boulders = np.array([first_boulder[0]+step_size, first_boulder[1]+(step_size*action)])
				else:
					more_boulders = np.array([first_boulder[0], first_boulder[1]+(step_size*action)])
				boulder_coords.append(more_boulders)
		else:
			first_boulder = [second_fruit[0], second_fruit[1]-step_size]
			boulder_coordinates = [first_boulder]
			for action in range(1, enforcer_action[1]):
				if action == 2:
					more_boulders = np.array([first_boulder[0]+(step_size*action), first_boulder[1]+step_size])
				else:
					more_boulders = np.array([first_boulder[0]+(step_size*action), first_boulder[1]])
				boulder_coordinates.append(more_boulders)

	# If the agent starts off on the bottom-right corner.
	elif index == 1:
		# Update the fruit coordinates.
		first_fruit -= np.array([0.0, 6.0-natural_cost[0]*step_size])
		second_fruit += np.array([6.0-natural_cost[1]*step_size, 0.0])

		# The enforcer either does nothing, raises the cost of the first
		# fruit, or raises the cost of the second fruit.
		if sum(enforcer_action) == 0:
			boulder_coords = None
		elif np.argmax(enforcer_action) == 0:
			first_boulder = [first_fruit[0], first_fruit[1]-step_size]
			boulder_coords = [first_boulder]
			for action in range(1, enforcer_action[0]):
				if action == 2:
					more_boulders = np.array([first_boulder[0]-(step_size*action), first_boulder[1]+step_size])
				else:
					more_boulders = np.array([first_boulder[0]-(step_size*action), first_boulder[1]])
				boulder_coords.append(more_boulders)
		else:
			first_boulder = [second_fruit[0]+step_size, second_fruit[1]]
			boulder_coords = [first_boulder]
			for action in range(1, enforcer_action[1]):
				if action == 2:
					more_boulders = np.array([first_boulder[0]-step_size, first_boulder[1]+(step_size*action)])
				else:
					more_boulders = np.array([first_boulder[0], first_boulder[1]+(step_size*action)])
				boulder_coords.append(more_boulders)

	# If the agent starts off on the top-right corner.
	elif index == 2:
		# Update the fruit coordinates.
		first_fruit += np.array([6.0-natural_cost[0]*step_size, 0.0])
		second_fruit += np.array([0.0, 6.0-natural_cost[1]*step_size])

		# The enforcer either does nothing, raises the cost of the first
		# fruit, or raises the cost of the second fruit.
		if sum(enforcer_action) == 0:
			boulder_coords = None
		elif np.argmax(enforcer_action) == 0:
			first_boulder = [first_fruit[0]+step_size, first_fruit[1]]
			boulder_coords = [first_boulder]
			for action in range(1, enforcer_action[0]):
				if action == 2:
					more_boulders = np.array([first_boulder[0]-step_size, first_boulder[1]-(step_size*action)])
				else:	
					more_boulders = np.array([first_boulder[0], first_boulder[1]-(step_size*action)])
				boulder_coords.append(more_boulders)
		else:
			first_boulder = [second_fruit[0], second_fruit[1]+step_size]
			boulder_coords = [first_boulder]
			for action in range(1, enforcer_action[1]):
				if action == 2:
					more_boulders = np.array([first_boulder[0]-(step_size*action), first_boulder[1]-step_size])
				else:
					more_boulders = np.array([first_boulder[0]-(step_size*action), first_boulder[1]])
				boulder_coords.append(more_boulders)

	# If the agent starts off on the top-left corner.
	else:
		# Update the fruit coordinates.
		first_fruit += np.array([0.0, 6.0-natural_cost[0]*step_size])
		second_fruit -= np.array([6.0-natural_cost[1]*step_size, 0.0])

		# The enforcer either does nothing, raises the cost of the first
		# fruit, or raises the cost of the second fruit.
		if sum(enforcer_action) == 0:
			boulder_coords = None
		elif np.argmax(enforcer_action) == 0:
			first_boulder = [first_fruit[0], first_fruit[1]+step_size]
			boulder_coords = [first_boulder]
			for action in range(1, enforcer_action[0]):
				if action == 2:
					more_boulders = np.array([first_boulder[0]+(step_size*action), first_boulder[1]-step_size])
				else:	
					more_boulders = np.array([first_boulder[0]+(step_size*action), first_boulder[1]])
				boulder_coords.append(more_boulders)
		else:
			first_boulder = [second_fruit[0]-step_size, second_fruit[1]]
			boulder_coord  = [first_boulder]
			for action in range(1, enforcer_action[1]):
				if action == 2:
					more_boulders = np.array([first_boulder[0]+step_size, first_boulder[1]-(step_size*action)])
				else:
					more_boulders = np.array([first_boulder[0], first_boulder[1]-(step_size*action)])
				boulder_coords.append(more_boulders)

	if pear_corner == coords[index]["fruit"][0]:
		return first_fruit, second_fruit, boulder_coords
	else:
		return second_fruit, first_fruit, boulder_coords

if __name__ == "__main__":
	# Set up how the stimuli will be varied.
	coords = {
		0: {"agent": [0.5, 0.5], "fruit": [[6.5, 0.5], [0.5, 6.5]]},
		1: {"agent": [7.5, 0.5], "fruit": [[6.5, 6.5], [0.5, 0.5]]},
		2: {"agent": [7.5, 7.5], "fruit": [[0.5, 6.5], [6.5, 0.5]]},
		3: {"agent": [0.5, 7.5], "fruit": [[0.5, 0.5], [6.5, 6.5]]},					
	}
	boulders = {
		0: [[1.5, 2.5], [7.5, 5.5], [4.5, 6.5]],
		1: [[5.5, 1.5], [2.5, 7.5], [1.5, 4.5]],
		2: [[6.5, 5.5], [0.5, 2.5], [3.5, 1.5]],
		3: [[2.5, 6.5], [5.5, 0.5], [6.5, 3.5]]
	}
	natural_costs = np.array(list(it.product([4, 5, 6], repeat=2)))
	enforcer_actions = np.array([[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]])
	step_size = 1.0

	# Create the stimuli by iterating through all potential combinations of 
	# agent and fruit positions, creating a tex file, converting it to a pdf 
	# file, then converting that to a png file, and then finally renaming it.
	for index in coords:
		if index != 3:
			continue
		agent_coords = coords[index]["agent"]
		grass = "grass_" + str(index)
		fruit_corners = coords[index]["fruit"]
		for pear_corner in fruit_corners:
			pomegranate_corner = [pomegranate_corner for pomegranate_corner in fruit_corners \
								  if pomegranate_corner != pear_corner][0]
			path = str(np.array(agent_coords)) + "/" + str(np.array(pear_corner)) + "/"
			for natural_cost in natural_costs:
				for enforcer_action in enforcer_actions:
					filename = str(natural_cost) + "_" + str(enforcer_action)
					pear_coords, pomegranate_coords, boulder_coords = get_coords(index, pear_corner, pomegranate_corner, \
																		natural_cost, enforcer_action, step_size)
					with open(path + filename + ".tex", "w", newline="") as file: 
						file.write("\\documentclass{standalone}\n\n" + \
								   "\\usepackage{tikz}\n" + \
								   "\\usepackage{graphicx}\n" + \
								   "\\graphicspath{{D:/Research/social_pragmatics/imgs/observer_1/}}\n\n" + \
								   "\\begin{document}\n" + \
								   "\\begin{tikzpicture}\n")
						file.write("\\node[anchor=south west,inner sep=0] at (0,0) " + \
							"{\\includegraphics[width=12.99cm, keepaspectratio]{%s}};\n" % \
							(grass))
						file.write("\\begin{scope}[shift={(2.5, 0.5)}]\n" + \
								   "\\draw[step=1.0cm,color=black, fill=white] (0,0) grid (8,8) rectangle (0,0);\n")
						file.write("\\node at (%f,%f) {\\includegraphics[scale=0.17]{hiker}};\n" % \
							(agent_coords[0], agent_coords[1]))
						file.write("\\node at (%f,%f) {\\includegraphics[scale=0.035]{pear}};\n" % \
							(pear_coords[0], pear_coords[1]))
						file.write("\\node at (%f,%f) {\\includegraphics[scale=0.035]{pear}};\n" % \
							(pear_coords[0]+step_size, pear_coords[1]))
						file.write("\\node at (%f,%f) {\\includegraphics[scale=0.035]{pear}};\n" % \
							(pear_coords[0], pear_coords[1]+step_size))
						file.write("\\node at (%f,%f) {\\includegraphics[scale=0.035]{pear}};\n" % \
							(pear_coords[0]+step_size, pear_coords[1]+step_size))
						file.write("\\node at (%f,%f) {\\includegraphics[scale=0.035]{pomegranate}};\n" % \
							(pomegranate_coords[0], pomegranate_coords[1]))
						file.write("\\node at (%f,%f) {\\includegraphics[scale=0.035]{pomegranate}};\n" % \
							(pomegranate_coords[0]+step_size, pomegranate_coords[1]))
						file.write("\\node at (%f,%f) {\\includegraphics[scale=0.035]{pomegranate}};\n" % \
							(pomegranate_coords[0], pomegranate_coords[1]+step_size))
						file.write("\\node at (%f,%f) {\\includegraphics[scale=0.035]{pomegranate}};\n" % \
							(pomegranate_coords[0]+step_size, pomegranate_coords[1]+step_size))
						file.write("\\node at (%f,%f) {\includegraphics[scale=0.20]{boulder_0.png}};\n" % \
							(boulders[index][0][0], boulders[index][0][1]))
						file.write("\\node at (%f,%f) {\includegraphics[scale=0.20]{boulder_0.png}};\n" % \
							(boulders[index][1][0], boulders[index][1][1]))
						file.write("\\node at (%f,%f) {\includegraphics[scale=0.20]{boulder_0.png}};\n" % \
							(boulders[index][2][0], boulders[index][2][1]))
						if sum(enforcer_action) != 0:
							for action in range(max(enforcer_action)):
								if len(np.shape(boulder_coords)) == 1:
									if index == 1:
										boulder_coords[0] += 1
									elif index == 2:
										boulder_coords[0] += 1
										boulder_coords[1] += 1
									elif index == 3:
										boulder_coords[1] += 1
									file.write("\\draw[step=1.0cm,color=red,fill=white,line width=0.7mm] " + \
											   "(%d,%d) rectangle (%d,%d);\n" % \
										(boulder_coords[0]-(step_size/2.0), boulder_coords[1]-(step_size/2.0), \
										 boulder_coords[0]+(step_size/2.0), boulder_coords[1]+(step_size/2.0)))
									file.write("\\node at (%f,%f) {\\includegraphics[scale=0.19]{boulder_2}};\n" % \
										(boulder_coords[0], boulder_coords[1]))
								else:
									if index == 1:
										boulder_coords[action][0] += 1
									elif index == 2:
										boulder_coords[action][0] += 1
										boulder_coords[action][1] += 1
									elif index == 3:
										boulder_coords[action][1] += 1
									file.write("\\draw[step=1.0cm,color=red,fill=white,line width=0.7mm] " + \
											   "(%d,%d) rectangle (%d,%d);\n" % \
										(boulder_coords[action][0]-(step_size/2.0), boulder_coords[action][1]-(step_size/2.0), \
										 boulder_coords[action][0]+(step_size/2.0), boulder_coords[action][1]+(step_size/2.0)))
									file.write("\\node at (%f,%f) {\\includegraphics[scale=0.19]{boulder_2}};\n" % \
										(boulder_coords[action][0], boulder_coords[action][1]))
						file.write("\\end{scope}\n" + \
								   "\\end{tikzpicture}\n" + \
								   "\\end{document}\n")
					os.system("pdflatex " + "\"" + path + filename + ".tex\"")
					os.system("pdftoppm -r 300 -png " + "\"" + filename + ".pdf\" " + "\"" + path + filename + "\"")
					os.chdir(path)
					os.system("rename " + "\"" + filename + "-1.png\"" + " \"" + filename + ".png\"")
					os.chdir("../../")
