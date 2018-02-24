import numpy as np
import os

def get_coords(index, natural_cost, enforcer_action):


# Set up how the stimuli will be varied.
genders = ["male", "female"]
coords = {
	0: {"agent": [1, 1], "fruit": [[9, 1], [1, 9]]},
	1: {"agent": [9, 1], "fruit": [[1, 1], [9, 9]]},
	2: {"agent": [9, 9], "fruit": [[1, 9], [9, 1]]},
	3: {"agent": [1, 9], "fruit": [[9, 9], [1, 1]]},					
}
natural_costs = np.array([[2, 2], [2, 3], [3, 2], [3, 3], [2, 4], [4, 2], [3, 4], [4, 3], [4, 4]])
enforcer_actions = np.array([[0, 0], [1, 0], [2, 0], [3, 0]])

# Create the stimuli by iterating through all potential combinations of agent
# genders and agent and fruit positions, creating a tex file, converting it to
# a pdf file, then converting that to a png file, and then finally renaming it.
for gender in genders:
	for index in positions:
		agent_coords = coords[index]["agent"]
		agent_direction = 1 if index == 0 or index == 3 else 0
		grass = "grass_" + str(index)
		fruit_coords = coords[index]["fruit"]
		for banana_coords in fruit_coords:
			path = "imgs/observer_1/" + gender + "/" + str(np.array(agent_coords)) + "/" + str(np.array(fruit_coords)) + "/"
			pear_coords = [pear_coords for pear_coords in fruit_coords if pear_coords != banana_coords]
			for natural_cost in natural_costs:
				for enforcer_action in enforcer_actions:
					filename = str(natural_cost) + "_" + str(enforcer_action)
					banana_coords, pear_coords, rock_coords = get_coords(index, natural_cost, enforcer_action)
					agent_scaling = 0.12 if gender == "male" else 0.37
					with open(path + filename + ".tex", "w", newline="") as file: 
						file.write("\\documentclass{standalone}\n\n \
									\\usepackage{tikz}\n \
									\\usepackage{graphicx}\n \
									\\graphicspath{{D:/Research/social_pragmatics/imgs/}}\n\n \
									\\begin{document}\n \
									\\begin{tikzpicture}\n")
						file.write("\\node[anchor=south west,inner sep=0] at (0,0) {\\includegraphics[scale=1.0]{%s}};\n" % (grass))
						file.write("\\begin{scope}[shift={(1.9, 0.43)}]\n \
									\\draw[step=2.0cm,color=black, fill=white] (0,0) grid (10,10) rectangle (0,0);\n")
						file.write("\\node at (%d,%d) {\\scalebox{%d}[1]{\\includegraphics[scale=%f]{%s}}};\n" % \
							(agent_position[0], agent_position[1], agent_direction, agent_scaling, gender))
						file.write("\\node at (%d,%d) {\\includegraphics[scale=0.25]{banana}};\n" % \
							(banana_coords[0], banana_coords[1]))
						file.write("\\node at (%d,%d) {\\includegraphics[scale=0.25]{pear}};\n" % \
							(pear_coords[0], pear_coords[1]))
						if sum(enforcer_action) != 0:
							for action in range(max(enforcer_action)):
								if len(np.shape(rock_coords)) == 1:
									file.write("\\node at (%d,%d) {\\includegraphics[scale=1.2]{rock}};\n" % \
										(rock_coords[0], rock_coords[1]))
								else:
									file.write("\\node at (%d,%d) {\\includegraphics[scale=1.2]{rock}};\n" % \
										(rock_coords[action][0], rock_coords[action][1]))
						file.write("\\end{scope}\n \
									\\end{tikzpicture}\n \
									\\end{document}\n")
					os.system("pdflatex " + path + "\"" + filename + ".tex\"")
					os.system("pdftoppm " + "\"" + filename + ".pdf\" " + path + "\"" + filename + "\"" + " -png")
					os.chdir("D:/Research/social_pragmatics/" + path)
					os.system("rename " + "\"" + filename + "-1.png\" \"" + filename + ".png\"")
					os.chdir("D:/Research/social_pragmatics/")
