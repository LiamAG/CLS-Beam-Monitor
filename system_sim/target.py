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
	"""
	Target object defining a simply scintillating target
	Inputs:
		str shape:  Specifies the shape of the target, supports
				    prism and circle
		tuple dims: Tuple specifying the dimensions of the target

	Attributes:
		float length: the length of the target in mm
		float width:  the width of the target in mm
		float depth:  the depth of the target in mm

		float radius: radius of a circlular target

		float light_output: light output by the target in photons/keV
		float tau_decay_ns: slow decay time of the material in ns

	Methods:
		incidence: models the incidence of an electron beam on the target
				   returns an np.ndarray object storing the number of
				   photons produced by the beam distributed over the target
				   dimensions
	"""
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

		# Assume linear response to electrons
		# ie. 40 photons/keV deposited (NaI(Tl))
		self.light_output = 40  # photons/keV
		self.tau_decay_ns = 70  # Ce:YAG

	def incidence(self, beam):
		"""
		Models the process of scintillation when an electron beam is
		incident on the target
		Inputs:
			beam: a beam object as defined in the beam module
		Outputs:
			photons: a numpy array containing the photons produced
					 by the beam
		"""
		profile = beam.profile
		energy = beam.energy
		photons = np.zeros((beam.dims))
		photons = profile * energy * self.light_output

		return photons
