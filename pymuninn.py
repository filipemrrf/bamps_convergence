from dataclasses import dataclass
import numpy as np
from scipy.interpolate import griddata
import pickle

class MuninnData:

#	def __init__(self, filenames: [str]):
#		points = []
#		values = []
#		times = set()
#
#		time = 0.0
#		for filename in filenames:
#			with open(filename) as file:
#				for line in file:
#					if line.startswith("\"Time ="):
#						words = line.split()
#						time = float(words[2])
#						times.add(time)
#						
#					# Skip commented and empty lines
#					elif line.startswith("\""):
#						continue
#
#					else:
#						words = line.split()
#						if words == []: # skip empty lines
#							continue
#						x = float(words[0])
#						y = float(words[1])
#						points.append([time,x])
#						values.append(y)
#
#		self.points = np.array(points)
#		self.values = np.array(values)
#		self.times = sorted(times)

	def __init__(self, filename):
		points = []
		values = []
		times = set()

		time = 0.0
		with open(filename) as file:
			for line in file:
				if line.startswith("\"Time ="):
					words = line.split()
					time = float(words[2])
					times.add(time)
					
				# Skip commented and empty lines
				elif line.startswith("\""):
					continue

				else:
					words = line.split()
					if words == []: # skip empty lines
						continue
					x = float(words[0])
					y = float(words[1])
					points.append([time,x])
					values.append(y)

		self.points = np.array(points)
		self.values = np.array(values)
		self.times = sorted(times)

	def as_grid(self):
		lines = {} # addressed by time

		# Prepare empty lists
		for time in self.times:
			lines[time] = []

		# Add data points to lists
		for i, [time, x] in enumerate(self.points):
			lines[time].append((x, self.values[i]))

		# Sort lines
		for (t, l) in lines.items():
			l.sort(key = lambda x : x[0])

		xss    = [np.array([x for (x, y) in lines[t]]) for t in self.times]
		values = [np.array([y for (x, y) in lines[t]]) for t in self.times]

		return MuninnDataGrid(self.times, xss, values)

	def interpolate_2d(self, ts: [float], xs: [float]):
		tt, xx = np.meshgrid(ts, xs)
		txs = np.array((tt.ravel(), xx.ravel())).T
		values = griddata(self.points, self.values, txs)
		return MuninnDataGridRegular(np.array(ts), np.array(xs), values.reshape(len(ts), len(xs)).T)

	def interpolate_x(self, xs: [float]):
		return self.interpolate_2d(xs, self.times)

	def at(self, time: float, x: float):
		return griddata(self.points, self.values, [time, x])[0]

@dataclass
class MuninnDataGrid:
	ts: np.ndarray
	xss: [np.ndarray]
	values: [np.ndarray]

class MuninnDataGridRegular:
	ts: np.ndarray
	xs: np.ndarray
	values: np.ndarray

	def __init__(self, ts: np.ndarray, xs: np.ndarray, values: np.ndarray):
		self.ts = ts
		self.xs = xs
		self.values = values

	@classmethod
	def from_data(cls, data: MuninnData, ts: [float], xs: [float]):
		# Turn raw data into grid with ordered timesteps
		grid_data = data.as_grid()

		# Within each timestep, interpolate onto regular spatial grid
		lines = np.array([np.interp(xs, grid_data.xss[i], grid_data.values[i]) for i,_ in enumerate(grid_data.ts)]) # I like functional style, sue me

		# Along each x-value, interpolate in time to get the final grid
		values = np.array([np.interp(ts, grid_data.ts, line) for line in lines.T])

		return cls(ts, xs, values.T)


	def at(self, time: float, x: float):
		# If data exists for the exact time, only interpolate in space
		if time in self.ts:
			i, = self.ts.where(np.isclose(self.ts, time))
			return np.interp(x, self.xs, self.values[i])
		# Otherwise, first interpolate in time, then in space
		else:
			line = [np.interp(time, self.ts, fs) for fs in self.values.T]
			return np.interp(x, self.xs, line)

def save(x, filename: str):
	with open(filename, "wb") as file:
		file.write(pickle.dumps(x))

def load(filename: str):
	with open(filename, "rb") as file:
		return pickle.loads(file.read())


def main():
	return

if __name__ == "__main__":
	main()
