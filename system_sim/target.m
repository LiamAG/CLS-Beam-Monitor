function [photon_mat] = target(beam_mat, tau_fast, tau_slow, photon_conversion)
% target models the interaction of the electron beam with the target screen
%   This function models the photons emitted from the target screen both
%   spatially and in time. The time resolution matches that of the beam
%   matrix generated at the beginning of the simulation script.

% TODO: Figure out how the decay time can be properly used

photon_mat = beam_mat * photon_conversion;

end