import numpy as np
import os

def generate_stimuli(natural_cost, enforcer_action):
	corners = np.array([[1.0, 1.0], [9.0, 1.0], [9.0, 9.0], [1.0, 9.0]])
	indices = np.arange(len(corners))
	agent_index = np.random.choice(indices)
	rock_coordinates = None
	agent_coordinates = corners[agent_index]
	if agent_index == 0:
		index = np.random.choice([1, 3])
		if index == 1:
			banana_coordinates = corners[index] - np.array([8.0-(natural_cost[0]*2.0), 0.0])
			pear_coordinates = corners[3] - np.array([0.0, 8.0-(natural_cost[1]*2.0)])
			if sum(enforcer_action) == 0:
				pass
			elif np.argmax(enforcer_action) == 0:
				first_rock = [banana_coordinates[0]-2.0, 1.0]
				rock_coordinates = [first_rock]
				for action in np.arange(enforcer_action[0]):
					if action == 0:
						continue
					more_rocks = np.array([first_rock[0], first_rock[1]+(2.0*action)])
					rock_coordinates.append(more_rocks)
			else:
				first_rock = [1.0, pear_coordinates[1]-2.0]
				rock_coordinates = [first_rock]
				for action in np.arange(enforcer_action[1]):
					if action == 0:
						continue
					more_rocks = np.array([first_rock[0]+(2.0*action), first_rock[1]])
					rock_coordinates.append(more_rocks)
		else:
			banana_coordinates = corners[index] - np.array([0.0, 8.0-(natural_cost[0]*2.0)])
			pear_coordinates = corners[1] - np.array([8.0-(natural_cost[1]*2.0), 0.0])
			if sum(enforcer_action) == 0:
				pass
			elif np.argmax(enforcer_action) == 0:
				first_rock = [1.0, banana_coordinates[1]-2.0]
				rock_coordinates = [first_rock]
				for action in np.arange(enforcer_action[0]):
					if action == 0:
						continue
					more_rocks = np.array([first_rock[0]+(2.0*action), first_rock[1]])
					rock_coordinates.append(more_rocks)
			else:
				first_rock = [pear_coordinates[0]-2.0, 1.0]
				rock_coordinates = [first_rock]
				for action in np.arange(enforcer_action[1]):
					if action == 0:
						continue
					more_rocks = np.array([first_rock[0], first_rock[1]+(2.0*action)])
					rock_coordinates.append(more_rocks)
	elif agent_index == 1:
		index = np.random.choice([0, 2])
		if index == 0:
			banana_coordinates = corners[index] + np.array([8.0-(natural_cost[0]*2.0), 0.0])
			pear_coordinates = corners[2] - np.array([0.0, 8.0-(natural_cost[1]*2.0)])
			if sum(enforcer_action) == 0:
				pass
			elif np.argmax(enforcer_action) == 0:
				first_rock = [banana_coordinates[0]+2.0, 1.0]
				rock_coordinates = [first_rock]
				for action in np.arange(enforcer_action[0]):
					if action == 0:
						continue
					more_rocks = np.array([first_rock[0], first_rock[1]+(2.0*action)])
					rock_coordinates.append(more_rocks)
			else:
				first_rock = [9.0, pear_coordinates[1]-2.0]
				rock_coordinates = [first_rock]
				for action in np.arange(enforcer_action[1]):
					if action == 0:
						continue
					more_rocks = np.array([first_rock[0]-(2.0*action), first_rock[1]])
					rock_coordinates.append(more_rocks)
		else:
			banana_coordinates = corners[index] - np.array([0.0, 8.0-(natural_cost[0]*2.0)])
			pear_coordinates = corners[0] + np.array([8.0-(natural_cost[1]*2.0), 0.0])
			if sum(enforcer_action) == 0:
				pass
			elif np.argmax(enforcer_action) == 0:
				first_rock = [9.0, banana_coordinates[1]-2.0]
				rock_coordinates = [first_rock]
				for action in np.arange(enforcer_action[0]):
					if action == 0:
						continue
					more_rocks = np.array([first_rock[0]-(2.0*action), first_rock[1]])
					rock_coordinates.append(more_rocks)
			else:
				first_rock = [pear_coordinates[0]+2.0, 1.0]
				rock_coordinates = [first_rock]
				for action in np.arange(enforcer_action[1]):
					if action == 0:
						continue
					more_rocks = np.array([first_rock[0], first_rock[1]+(2.0*action)])
					rock_coordinates.append(more_rocks)
	elif agent_index == 2:
		index = np.random.choice([1, 3])
		if index == 1:
			banana_coordinates = corners[index] + np.array([0.0, 8.0-(natural_cost[0]*2.0)])
			pear_coordinates = corners[3] + np.array([8.0-(natural_cost[1]*2.0), 0.0])
			if sum(enforcer_action) == 0:
				pass
			elif np.argmax(enforcer_action) == 0:
				first_rock = [9.0, banana_coordinates[1]+2.0]
				rock_coordinates = [first_rock]
				for action in np.arange(enforcer_action[0]):
					if action == 0:
						continue
					more_rocks = np.array([first_rock[0]-(2.0*action), first_rock[1]])
					rock_coordinates.append(more_rocks)
			else:
				first_rock = [pear_coordinates[0]+2.0, 9.0]
				rock_coordinates = [first_rock]
				for action in np.arange(enforcer_action[1]):
					if action == 0:
						continue
					more_rocks = np.array([first_rock[0], first_rock[1]-(2.0*action)])
					rock_coordinates.append(more_rocks)
		else:
			banana_coordinates = corners[index] + np.array([8.0-(natural_cost[0]*2.0), 0.0])
			pear_coordinates = corners[1] + np.array([0.0, 8.0-(natural_cost[1]*2.0)])
			if sum(enforcer_action) == 0:
				pass
			elif np.argmax(enforcer_action) == 0:
				first_rock = [banana_coordinates[0]+2.0, 9.0]
				rock_coordinates = [first_rock]
				for action in np.arange(enforcer_action[0]):
					if action == 0:
						continue
					more_rocks = np.array([first_rock[0], first_rock[1]-(2.0*action)])
					rock_coordinates.append(more_rocks)
			else:
				first_rock = [9.0, pear_coordinates[1]+2.0]
				rock_coordinates = [first_rock]
				for action in np.arange(enforcer_action[1]):
					if action == 0:
						continue
					more_rocks = np.array([first_rock[0]-(2.0*action), first_rock[1]])
					rock_coordinates.append(more_rocks)
	else:
		index = np.random.choice([0, 2])
		if index == 0:
			banana_coordinates = corners[index] + np.array([0.0, 8.0-(natural_cost[0]*2.0)])
			pear_coordinates = corners[2] - np.array([8.0-(natural_cost[1]*2.0), 0.0])
			if sum(enforcer_action) == 0:
				pass
			elif np.argmax(enforcer_action) == 0:
				first_rock = [1.0, banana_coordinates[1]+2.0]
				rock_coordinates = [first_rock]
				for action in np.arange(enforcer_action[0]):
					if action == 0:
						continue
					more_rocks = np.array([first_rock[0]+(2.0*action), first_rock[1]])
					rock_coordinates.append(more_rocks)
			else:
				first_rock = [pear_coordinates[0]-2.0, 9.0]
				rock_coordinates = [first_rock]
				for action in np.arange(enforcer_action[1]):
					if action == 0:
						continue
					more_rocks = np.array([first_rock[0], first_rock[1]-(2.0*action)])
					rock_coordinates.append(more_rocks)
		else:
			banana_coordinates = corners[index] - np.array([8.0-(natural_cost[0]*2.0), 0.0])
			pear_coordinates = corners[0] + np.array([0.0, 8.0-(natural_cost[1]*2.0)])
			if sum(enforcer_action) == 0:
				pass
			elif np.argmax(enforcer_action) == 0:
				first_rock = [banana_coordinates[0]-2.0, 9.0]
				rock_coordinates = [first_rock]
				for action in np.arange(enforcer_action[0]):
					if action == 0:
						continue
					more_rocks = np.array([first_rock[0], first_rock[1]-(2.0*action)])
					rock_coordinates.append(more_rocks)
			else:
				first_rock = [1.0, pear_coordinates[1]+2.0]
				rock_coordinates = [first_rock]
				for action in np.arange(enforcer_action[1]):
					if action == 0:
						continue
					more_rocks = np.array([first_rock[0]+(2.0*action), first_rock[1]])
					rock_coordinates.append(more_rocks)

	return agent_coordinates, banana_coordinates, pear_coordinates, rock_coordinates

natural_costs = np.array([[2, 2], [2, 3], [3, 2], [3, 3], [2, 4], [4, 2], [3, 4], [4, 3], [4, 4]])
enforcer_actions = np.array([[0, 0], [1, 0], [2, 0], [3, 0]])
path = "imgs/stimuli/"
tex = ".tex"
pdf = ".pdf"
for natural_cost in natural_costs:
	for enforcer_action in enforcer_actions:
		agent_coordinates, banana_coordinates, pear_coordinates, rock_coordinates = generate_stimuli(natural_cost, enforcer_action)
		filename = str(natural_cost) + "_" + str(enforcer_action)
		with open(path + filename + tex, "w", newline="") as file: 
			file.write("\\documentclass{standalone}\n\n")
			file.write("\\usepackage{tikz}\n\\usepackage{graphicx}\n\\graphicspath{ {D:/Research/social_pragmatics/imgs/} }\n\n")
			file.write("\\begin{document}\n\\begin{tikzpicture}\n\\draw[step=2.0cm,color=black] (0.0,0.0) grid (10.0,10.0);\n")
			file.write("\\node at (%f,%f) {\\includegraphics[scale=0.12]{agent}};\n" % (agent_coordinates[0], agent_coordinates[1]))
			file.write("\\node at (%f,%f) {\\includegraphics[scale=0.25]{banana}};\n" % (banana_coordinates[0], banana_coordinates[1]))
			file.write("\\node at (%f,%f) {\\includegraphics[scale=0.25]{pear}};\n" % (pear_coordinates[0], pear_coordinates[1]))
			if sum(enforcer_action) != 0:
				for action in np.arange(max(enforcer_action)):
					if len(np.shape(rock_coordinates)) == 1:
						file.write("\\node at (%f,%f) {\\includegraphics[scale=0.12]{rocks}};\n" % (rock_coordinates[0], rock_coordinates[1]))
					else:
						file.write("\\node at (%f,%f) {\\includegraphics[scale=0.12]{rocks}};\n" % (rock_coordinates[action][0], rock_coordinates[action][1]))
			file.write("\\end{tikzpicture}\n\\end{document}\n")
		os.system("pdflatex " + path + "\"" + filename + tex + "\"")
		os.system("pdftoppm " + "\"" + str(natural_cost) + "_" + str(enforcer_action) + pdf + "\"" + " " + path + \
				  "\"" + str(natural_cost) + "_" + str(enforcer_action) + "\"" + " -png")
		os.chdir("D:/Research/social_pragmatics/" + path)
		os.system("rename " + "\"" + str(natural_cost) + "_" + str(enforcer_action) + \
				  "-1.png" + "\" " + "\""+ str(natural_cost) + "_" + str(enforcer_action) + ".png" + "\"")
		os.chdir("D:/Research/social_pragmatics/")
