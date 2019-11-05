# File: target.py
# 
# (c) Liam Graham -- 2019
# <Put your name here if you work on this file>
#
# Description:
# Code modelling a target object for use in simulating
# the transverse beam profile monitor for the CLS

import numpy as np


class target(object):
	"""docstring for target"""
	def __init__(self, shape: str, dims: tuple):
		"""initialization for target"""
		if shape == 'prism':
			self.length = dims[0]
			self.width = dims[1]
			self.depth = dims[2]
		elif shape == 'circle':
			self.radius = dims[0]
			self.depth = dims[1]
		else:
			raise TypeError('{} is not an supported target geometry'.format{shape})

		# Assume linear response to electrons and no decay time
		# ie. 40 photons/keV deposited (NaI(Tl))
		self.light_output = 40  # photons/keV
		self.flourescence_time_ns = 0
		self.tau_decay_ns = 70  # Ce:YAG
