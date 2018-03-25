import numpy as np
import os

def get_coords(index, apple_corner, pear_corner, natural_cost, enforcer_action):
	# Set the ordering of the fruits (counterclockwise from the agent).
	if apple_corner == coords[index]["fruit"][0]:
		first_fruit = apple_corner
		second_fruit = pear_corner
	else: 
		first_fruit = pear_corner
		second_fruit = apple_corner

	# If the agent starts off on the bottom-left corner.
	if index == 0:
		# Update the fruit coordinates.
		first_fruit -= np.array([8.0-natural_cost[0]*2.0, 0.0])
		second_fruit -= np.array([0.0, 8.0-natural_cost[1]*2.0])

		# The enforcer either does nothing, raises the cost of the first
		# fruit, or raises the cost of the second fruit.
		if sum(enforcer_action) == 0:
			rock_coords = None
		elif np.argmax(enforcer_action) == 0:
			first_rock = [first_fruit[0]-2.0, first_fruit[1]]
			rock_coords = [first_rock]
			for action in range(1, enforcer_action[0]):
				more_rocks = np.array([first_rock[0], first_rock[1]+(2.0*action)])
				rock_coords.append(more_rocks)
		else:
			first_rock = [second_fruit[0], second_fruit[1]-2.0]
			rock_coordinates = [first_rock]
			for action in range(1, enforcer_action[1]):
				more_rocks = np.array([first_rock[0]+(2.0*action), first_rock[1]])
				rock_coordinates.append(more_rocks)

	# If the agent starts off on the bottom-right corner.
	elif index == 1:
		# Update the fruit coordinates.
		first_fruit -= np.array([0.0, 8.0-natural_cost[0]*2.0])
		second_fruit += np.array([8.0-natural_cost[1]*2.0, 0.0])

		# The enforcer either does nothing, raises the cost of the first
		# fruit, or raises the cost of the second fruit.
		if sum(enforcer_action) == 0:
			rock_coords = None
		elif np.argmax(enforcer_action) == 0:
			first_rock = [first_fruit[0], first_fruit[1]-2.0]
			rock_coords = [first_rock]
			for action in range(1, enforcer_action[0]):
				more_rocks = np.array([first_rock[0]-(2.0*action), first_rock[1]])
				rock_coords.append(more_rocks)
		else:
			first_rock = [second_fruit[0]+2.0, second_fruit[1]]
			rock_coords = [first_rock]
			for action in range(1, enforcer_action[1]):
				more_rocks = np.array([first_rock[0], first_rock[1]+(2.0*action)])
				rock_coords.append(more_rocks)

	# If the agent starts off on the top-right corner.
	elif index == 2:
		# Update the fruit coordinates.
		first_fruit += np.array([8.0-natural_cost[0]*2.0, 0.0])
		second_fruit += np.array([0.0, 8.0-natural_cost[1]*2.0])

		# The enforcer either does nothing, raises the cost of the first
		# fruit, or raises the cost of the second fruit.
		if sum(enforcer_action) == 0:
			rock_coords = None
		elif np.argmax(enforcer_action) == 0:
			first_rock = [first_fruit[0]+2.0, first_fruit[1]]
			rock_coords = [first_rock]
			for action in range(1, enforcer_action[0]):
				more_rocks = np.array([first_rock[0], first_rock[1]-(2.0*action)])
				rock_coords.append(more_rocks)
		else:
			first_rock = [second_fruit[0], second_fruit[1]+2.0]
			rock_coords = [first_rock]
			for action in range(1, enforcer_action[1]):
				more_rocks = np.array([first_rock[0]-(2.0*action), first_rock[1]])
				rock_coords.append(more_rocks)

	# If the agent starts off on the top-left corner.
	else:
		# Update the fruit coordinates.
		first_fruit += np.array([0.0, 8.0-natural_cost[0]*2.0])
		second_fruit -= np.array([8.0-natural_cost[1]*2.0, 0.0])

		# The enforcer either does nothing, raises the cost of the first
		# fruit, or raises the cost of the second fruit.
		if sum(enforcer_action) == 0:
			rock_coords = None
		elif np.argmax(enforcer_action) == 0:
			first_rock = [first_fruit[0], first_fruit[1]+2.0]
			rock_coords = [first_rock]
			for action in range(1, enforcer_action[0]):
				more_rocks = np.array([first_rock[0]+(2.0*action), first_rock[1]])
				rock_coords.append(more_rocks)
		else:
			first_rock = [second_fruit[0]-2.0, second_fruit[1]]
			rock_coord  = [first_rock]
			for action in range(1, enforcer_action[1]):
				more_rocks = np.array([first_rock[0], first_rock[1]-(2.0*action)])
				rock_coords.append(more_rocks)

	if apple_corner == coords[index]["fruit"][0]:
		return first_fruit, second_fruit, rock_coords
	else:
		return second_fruit, first_fruit, rock_coords

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
		if index == 0 or index == 2 or index == 3:
			continue
		agent_coords = coords[index]["agent"]
		grass = "grass_" + str(index)
		fruit_corners = coords[index]["fruit"]
		for apple_corner in fruit_corners:
			pear_corner = [pear_corner for pear_corner in fruit_corners if pear_corner != apple_corner][0]
			path = "../imgs/observer_1/" + str(np.array(agent_coords)) + "/" + str(np.array(apple_corner)) + "/"
			for natural_cost in natural_costs:
				for enforcer_action in enforcer_actions:
					filename = str(natural_cost) + "_" + str(enforcer_action)
					apple_coords, pear_coords, rock_coords = get_coords(index, apple_corner, pear_corner, \
																		natural_cost, enforcer_action)
					with open(path + filename + ".tex", "w", newline="") as file: 
						file.write("\\documentclass{standalone}\n\n" + \
								   "\\usepackage{tikz}\n" + \
								   "\\usepackage{graphicx}\n" + \
								   "\\graphicspath{{D:/Research/social_pragmatics/imgs/}}\n\n" + \
								   "\\begin{document}\n" + \
								   "\\begin{tikzpicture}\n")
						file.write("\\node[anchor=south west,inner sep=0] at (0,0) {\\includegraphics[scale=1.0]{%s}};\n" % \
							(grass))
						file.write("\\begin{scope}[shift={(1.9, 0.43)}]\n" + \
								   "\\draw[step=2.0cm,color=black, fill=white] (0,0) grid (10,10) rectangle (0,0);\n")
						file.write("\\node at (%d,%d) {\\includegraphics[scale=1.0]{agent}};\n" % \
							(agent_coords[0], agent_coords[1]))
						file.write("\\node at (%d,%d) {\\includegraphics[scale=0.06]{apple}};\n" % \
							(apple_coords[0], apple_coords[1]))
						file.write("\\node at (%d,%d) {\\includegraphics[scale=0.7]{pear}};\n" % \
							(pear_coords[0], pear_coords[1]))
						if sum(enforcer_action) != 0:
							for action in range(max(enforcer_action)):
								if len(np.shape(rock_coords)) == 1:
									file.write("\\node at (%d,%d) {\\includegraphics[scale=1.2]{rock}};\n" % \
										(rock_coords[0], rock_coords[1]))
								else:
									file.write("\\node at (%d,%d) {\\includegraphics[scale=1.2]{rock}};\n" % \
										(rock_coords[action][0], rock_coords[action][1]))
						file.write("\\end{scope}\n" + \
								   "\\end{tikzpicture}\n" + \
								   "\\end{document}\n")
					os.system("pdflatex " + "\"" + path + filename + ".tex\"")
					os.system("pdftoppm -r 300 -png " + "\"" + filename + ".pdf\" " + "\"" + path + filename + "\"")
					os.chdir(path)
					os.system("rename " + "\"" + filename + "-1.png\" \"" + filename + ".png\"")
					os.chdir("../utils")
