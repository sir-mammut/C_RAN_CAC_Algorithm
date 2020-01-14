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
		This is C-RAN CAC Algorithm.
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
			1	:	20,
			2	:	30,
			3	:	40,
			4	:	50,
			5	:	500
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
		dict_of_bbu = self.__bbu()

		if request <= 0:
			# If the requested capacity is less than zero(0) return the actual dictionary
			return dict_of_bbu
		else:
			re = (-request)

			m = dict_of_bbu[0] + re
			if m < 0:
				dict_of_bbu[0] = 0
				i = 1
				while m < 0:
					m = dict_of_bbu[i] + m
					if m >= 0:
						dict_of_bbu[i] = m
					else:
						dict_of_bbu[i] = 0
					i+=1
				return dict_of_bbu
			else:
				dict_of_bbu[0] = m

				return dict_of_bbu

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

		d = {}

		if a_c > r_c:
			# No congestion
			# beginning BBU local resource checking
			bbuLoadList = sorted([n for n in self.bbuRetune(r_c).values()])
			# return bbuLoadList
			
			for i, j in self.__bbu().items():
				# Chcking remaining load levels
				# on the sorted BBU list
				if (self.__bbu()[i]) > r_c:
					# accept request
					d[i] = "BBU_{} acceptRequest;".format(i)
				else:
					# reject request
					d[i] = "BBU_{} rejectRequest;".format(i)
			return [n for n in d.values()]
		else:
			# Base station is congested
			# reject request
			d[i] = "BBU_{} rejectRequest;".format(i)

			return [n for n in d.values()]

if __name__ == '__main__':
	
	rc = C_RAN_CAC_Algorithm()

	print(rc.decisionMaker(20))

