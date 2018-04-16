import numpy as np
import os

def get_coords(index, pear_corner, pomegranate_corner, natural_cost, enforcer_action):
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
		first_fruit -= np.array([8.0-natural_cost[0]*2.0, 0.0])
		second_fruit -= np.array([0.0, 8.0-natural_cost[1]*2.0])

		# The enforcer either does nothing, raises the cost of the first
		# fruit, or raises the cost of the second fruit.
		if sum(enforcer_action) == 0:
			boulder_coords = None
		elif np.argmax(enforcer_action) == 0:
			first_boulder = [first_fruit[0]-2.0, first_fruit[1]]
			boulder_coords = [first_boulder]
			for action in range(1, enforcer_action[0]):
				if action == 2:
					more_boulders = np.array([first_boulder[0]+2.0, first_boulder[1]+(2.0*action)])
				else:
					more_boulders = np.array([first_boulder[0], first_boulder[1]+(2.0*action)])
				boulder_coords.append(more_boulders)
		else:
			first_boulder = [second_fruit[0], second_fruit[1]-2.0]
			boulder_coordinates = [first_boulder]
			for action in range(1, enforcer_action[1]):
				if action == 2:
					more_boulders = np.array([first_boulder[0]+(2.0*action), first_boulder[1]+2.0])
				else:
					more_boulders = np.array([first_boulder[0]+(2.0*action), first_boulder[1]])
				boulder_coordinates.append(more_boulders)

	# If the agent starts off on the bottom-right corner.
	elif index == 1:
		# Update the fruit coordinates.
		first_fruit -= np.array([0.0, 8.0-natural_cost[0]*2.0])
		second_fruit += np.array([8.0-natural_cost[1]*2.0, 0.0])

		# The enforcer either does nothing, raises the cost of the first
		# fruit, or raises the cost of the second fruit.
		if sum(enforcer_action) == 0:
			boulder_coords = None
		elif np.argmax(enforcer_action) == 0:
			first_boulder = [first_fruit[0], first_fruit[1]-2.0]
			boulder_coords = [first_boulder]
			for action in range(1, enforcer_action[0]):
				if action == 2:
					more_boulders = np.array([first_boulder[0]-(2.0*action), first_boulder[1]+2.0])
				else:
					more_boulders = np.array([first_boulder[0]-(2.0*action), first_boulder[1]])
				boulder_coords.append(more_boulders)
		else:
			first_boulder = [second_fruit[0]+2.0, second_fruit[1]]
			boulder_coords = [first_boulder]
			for action in range(1, enforcer_action[1]):
				if action == 2:
					more_boulders = np.array([first_boulder[0]-2.0, first_boulder[1]+(2.0*action)])
				else:
					more_boulders = np.array([first_boulder[0], first_boulder[1]+(2.0*action)])
				boulder_coords.append(more_boulders)

	# If the agent starts off on the top-right corner.
	elif index == 2:
		# Update the fruit coordinates.
		first_fruit += np.array([8.0-natural_cost[0]*2.0, 0.0])
		second_fruit += np.array([0.0, 8.0-natural_cost[1]*2.0])

		# The enforcer either does nothing, raises the cost of the first
		# fruit, or raises the cost of the second fruit.
		if sum(enforcer_action) == 0:
			boulder_coords = None
		elif np.argmax(enforcer_action) == 0:
			first_boulder = [first_fruit[0]+2.0, first_fruit[1]]
			boulder_coords = [first_boulder]
			for action in range(1, enforcer_action[0]):
				if action == 2:
					more_boulders = np.array([first_boulder[0]-2.0, first_boulder[1]-(2.0*action)])
				else:	
					more_boulders = np.array([first_boulder[0], first_boulder[1]-(2.0*action)])
				boulder_coords.append(more_boulders)
		else:
			first_boulder = [second_fruit[0], second_fruit[1]+2.0]
			boulder_coords = [first_boulder]
			for action in range(1, enforcer_action[1]):
				if action == 2:
					more_boulders = np.array([first_boulder[0]-(2.0*action), first_boulder[1]-2.0])
				else:
					more_boulders = np.array([first_boulder[0]-(2.0*action), first_boulder[1]])
				boulder_coords.append(more_boulders)

	# If the agent starts off on the top-left corner.
	else:
		# Update the fruit coordinates.
		first_fruit += np.array([0.0, 8.0-natural_cost[0]*2.0])
		second_fruit -= np.array([8.0-natural_cost[1]*2.0, 0.0])

		# The enforcer either does nothing, raises the cost of the first
		# fruit, or raises the cost of the second fruit.
		if sum(enforcer_action) == 0:
			boulder_coords = None
		elif np.argmax(enforcer_action) == 0:
			first_boulder = [first_fruit[0], first_fruit[1]+2.0]
			boulder_coords = [first_boulder]
			for action in range(1, enforcer_action[0]):
				if action == 2:
					more_boulders = np.array([first_boulder[0]+(2.0*action), first_boulder[1]-2.0])
				else:	
					more_boulders = np.array([first_boulder[0]+(2.0*action), first_boulder[1]])
				boulder_coords.append(more_boulders)
		else:
			first_boulder = [second_fruit[0]-2.0, second_fruit[1]]
			boulder_coord  = [first_boulder]
			for action in range(1, enforcer_action[1]):
				if action == 2:
					more_boulders = np.array([first_boulder[0]+2.0, first_boulder[1]-(2.0*action)])
				else:
					more_boulders = np.array([first_boulder[0], first_boulder[1]-(2.0*action)])
				boulder_coords.append(more_boulders)

	if pear_corner == coords[index]["fruit"][0]:
		return first_fruit, second_fruit, boulder_coords
	else:
		return second_fruit, first_fruit, boulder_coords

if __name__ == "__main__":
	# Set up how the stimuli will be varied.
	coords = {
		0: {"agent": [1, 1], "fruit": [[9, 1], [1, 9]]},
		1: {"agent": [9, 1], "fruit": [[9, 9], [1, 1]]},
		2: {"agent": [9, 9], "fruit": [[1, 9], [9, 1]]},
		3: {"agent": [1, 9], "fruit": [[1, 1], [9, 9]]},					
	}
	natural_costs = np.array([[2, 2], [2, 3], [3, 2], [3, 3], [2, 4], [4, 2], [3, 4], [4, 3], [4, 4]])
	enforcer_actions = np.array([[0, 0], [1, 0], [2, 0], [3, 0]])

	# Create the stimuli by iterating through all potential combinations of 
	# agent and fruit positions, creating a tex file, converting it to a pdf 
	# file, then converting that to a png file, and then finally renaming it.
	for index in coords:
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
																		natural_cost, enforcer_action)
					with open(path + filename + ".tex", "w", newline="") as file: 
						file.write("\\documentclass{standalone}\n\n" + \
								   "\\usepackage{tikz}\n" + \
								   "\\usepackage{graphicx}\n" + \
								   "\\graphicspath{{D:/Research/social_pragmatics/imgs/observer_1/}}\n\n" + \
								   "\\begin{document}\n" + \
								   "\\begin{tikzpicture}\n")
						file.write("\\node[anchor=south west,inner sep=0] at (0,0) {\\includegraphics[scale=1.0]{%s}};\n" % \
							(grass))
						file.write("\\begin{scope}[shift={(1.9, 0.43)}]\n" + \
								   "\\draw[step=2.0cm,color=black, fill=white] (0,0) grid (10,10) rectangle (0,0);\n")
						file.write("\\node at (%d,%d) {\\includegraphics[scale=0.3]{hiker}};\n" % \
							(agent_coords[0], agent_coords[1]))
						file.write("\\node at (%d,%d) {\\includegraphics[scale=0.07]{pear}};\n" % \
							(pear_coords[0], pear_coords[1]))
						file.write("\\node at (%d,%d) {\\includegraphics[scale=0.07]{pomegranate}};\n" % \
							(pomegranate_coords[0], pomegranate_coords[1]))
						if sum(enforcer_action) != 0:
							for action in range(max(enforcer_action)):
								if len(np.shape(boulder_coords)) == 1:
									file.write("\\node at (%d,%d) {\\includegraphics[scale=0.85]{boulder}};\n" % \
										(boulder_coords[0], boulder_coords[1]))
								else:
									file.write("\\node at (%d,%d) {\\includegraphics[scale=0.85]{boulder}};\n" % \
										(boulder_coords[action][0], boulder_coords[action][1]))
						file.write("\\end{scope}\n" + \
								   "\\end{tikzpicture}\n" + \
								   "\\end{document}\n")
					os.system("pdflatex " + "\"" + path + filename + ".tex\"")
					os.system("pdftoppm -r 300 -png " + "\"" + filename + ".pdf\" " + "\"" + path + filename + "\"")
					os.chdir(path)
					os.system("rename " + "\"" + filename + "-1.png\"" + " \"" + filename + ".png\"")
					os.chdir("../../")
