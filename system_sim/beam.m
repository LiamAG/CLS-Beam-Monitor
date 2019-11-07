function [beam_mat] = beam(diameter, charge, pulse_len, energy, distribution)
    % beam : function creating a matrix that models an electron pulse
    % Models an electron pulse by converting a total charge, pulse length,
    % and diameter into a series of nanosecond slices with electron energy
    % distributed over each slice according to the specified distribution
    % Inputs:
    %   diameter:     The diameter of the beam spot in milimetres
    %   charge:       The total charge contained in the pulse in Coulombs
    %   pulse_len:    The total time of the pulse in nanoseconds
    %   energy:       The electron energy in keV
    %   distribution: The electron spatial distribution of the modelled beam.
    %                 One of flat, Gauss, or linear. Represented as characters
    %                 'f', 'G', or 'l'
    % Outputs:
    %   beam_mat: a 2 dimensional matrix made up of the electron spatial
    %             distribution


end