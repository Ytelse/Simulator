
import numpy as np

class Ram:
	
	def __init__(self):
		self._memory = np.array([])
		self._accessHistory = [[]]
	
	def add_content(self,values):
		offset = len(self._memory)
		self._memory = np.append(self._memory,values)
		return offset
	
	def get_values(self,addr, width):
		r = self._memory[addr:addr + width]
		if len(r) < width:
			r = np.append(self._memory, [0] * width)
		
		self._accessHistory[-1].append(("read",addr,width))
		
		return r
	
	def put_values(self,addr,values):
		self._memory[addr:addr + len(values)] = values
		self._accessHistory[-1].append(("write",addr,len(values)))
		
	def tick(self):
		self._accessHistory.append([])
	
	def get_history(self):
		return self._accessHistory

	
