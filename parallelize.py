import csv
import multiprocessing as mp
import numpy as np

if __name__ == "__main__":
	# Observer inferring the enforcer's beliefs about the agent reward and degree of ToM (parallelized).
	start_time = time.time()
	NUM_PROCESSES = 4
	agent_rewards_set = np.split(agent_rewards, NUM_PROCESSES)
	processes = []
	output = mp.Queue()
	for p in np.arange(NUM_PROCESSES):
		kw = {"parallel": True, "enforcer_reward": enforcer_reward, "cooperation": cooperation, \
			  "enforcer_action": enforcer_action, "agent_rewards": agent_rewards_set[p], "output": output}
		processes.append(mp.Process(target=observer, args=("agent_reward_and_p", rationality), kwargs=kw))

	for process in processes:
		process.start()
	print("Started!")
	for process in processes:
		process.join()
		print("One process joined!")
	print("Done!")
	likelihood = np.vstack([output.get() for process in processes])

	# Normalize the likelihood to generate the posterior.
	likelihood = likelihood.flatten()
	if sum(likelihood) == 0:
		posterior = likelihood.reshape(space)
	else:
		posterior = (likelihood/sum(likelihood)).reshape(space)

	x4 = posterior
	print(time.time()-start_time)
	with open("temp.txt", "w", newline="") as file:
		writer = csv.writer(file)
		writer.writerows(x4)
