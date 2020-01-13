"""
C-RAN CAC Algorithm

BBU 	: baseband_unit

Ac 		: available_capacity
BBUl 	: current_BBU_load
BBUm 	: maximum_BBU_capacity
n 		: Total_number_of_BBUs
Rc 		: Requested_capacity
Tc		: total_system_capacity
		: new_request_arrival_rate
		: new_request_service_rate 

"""

class C_RAN_CAC_Algorithm(object):
	"""
		The Requested_capacity class will accept 2 parameters
		1. BBU = Baseband Unit and 
		2. Rc  = Requested capacity

	"""
	def __init__(self):
		super(C_RAN_CAC_Algorithm, self).__init__()

		self.__requested_capacity = 0
		self.accept_request = True
		
	def __bbu(self):
		"""Baseband Unit:
			contains a dictionary of BBUs and their corresponding capacities
			return: the entire dictionary
		"""
		self.baseband_unit = {
			0	:	10,
			1	:	200,
			2	:	20,
			3	:	30,
			4	:	40,
			5	:	50
		}

		return self.baseband_unit

	def n(self):
		"""
			Total number of BBUs
				return: number of BBUs
		"""
		bbu_num = len(self.__bbu())

		return bbu_num

	#---------------------------------------------------------#
	#This is the beggining of Global Cloud resources checking.#
	#---------------------------------------------------------#
	def totalSystemCapacity(self):
		"""Tc : otal system capacities"""
		self.tc = sum((self.__bbu().values()))

		return self.tc

	def bbuLoad(self):
		"""
			BBUl : BBU load
				is the capacity that is being utilized
		"""
		return self.__requested_capacity

	def availableCapacity(self):
		"""
			Ac : available capacities
				return: available capacities
		"""

		#tc stands for total capacity of the system.
		tc = self.totalSystemCapacity()

		#rc stands for BBU Load
		rc = self.bbuLoad()

		available_capacity = tc - rc

		return available_capacity


	def getRequestedCapacity(self, request):
		"""Rc : requested capacities
			is the sum of the given request and the BBUl of the system
		"""
		self.__requested_capacity += request


	# def bbuRetune(self):
		
	# 	bbuR = [n for n in self.__bbu().values()]

	# 	return sorted(bbuR)

	def bbuRetune(self, request):
		"""
			This function keeps tracks of BBUl.
			The function also return the sorted list of the BBUs based on their load level.

		"""

		dic = self.__bbu()

		if request <= 0:
			return 0
		else:
			newD = {}
			for x, y in dic.items():
				re = (-request)

				m = dic[x] + re
				newD[x] = m

				if m < 0:
					i = x
					while m < 0:
						m = dic[i+1] + m

						newD[x] = m
						if m >= 0:
							break
						i+=1
				elif m == 0:
					return newD
			return [n for n in newD.values()]

	def decisionMaker(self, r_capacity):
		"""
			CAC Decision Maker : 
				Decide whether to accept or reject the call request.
			Parameter:
			----------
				r_capacity : requested capacities
		"""
		a_c = self.availableCapacity();
		r_c = r_capacity

		if a_c > r_c:
			# No congestion
			#beginning BBU local resource checking
			bbuLoadList = sorted(self.bbuRetune(r_c))

			for i in self.n():
				#Chcking remaining load levels
				#on the sorted BBU list
				if (self.__bbu()[i]-bbuLoadList[i]) > r_c:
					return self.accept_request
				else:
					self.accept_request = False

					return self.accept_request
		else:
			#Base station is congested

			self.accept_request = False

			return self.accept_request

if __name__ == '__main__':
	
	rc = C_RAN_CAC_Algorithm()

	print(rc.bbuLoad())

