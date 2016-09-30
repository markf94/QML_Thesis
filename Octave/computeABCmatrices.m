function [A, B, C] = computeABCmatrices(beta, gamma, delta)

  %Compute the A Matrix
  theta_z = beta
  theta_y = gamma/2
  R_z = [exp(-i*theta_z/2) 0; 0 exp(i*theta_z/2)];
  R_y = [cos(theta_y/2) -sin(theta_y/2); sin(theta_y/2) cos(theta_y/2)]
  A = R_z*R_y;
  
  %Compute the B Matrix
  theta_z = -(delta+beta)/2
  theta_y = -gamma/2
  R_z = [exp(-i*theta_z/2) 0; 0 exp(i*theta_z/2)];
  R_y = [cos(theta_y/2) -sin(theta_y/2); sin(theta_y/2) cos(theta_y/2)];
  B = R_y*R_z;
  
  %Compute the C Matrix
  theta_z = (delta-beta)/2
  R_z = [exp(-i*theta_z/2) 0; 0 exp(i*theta_z/2)];
  C = R_z;
endfunction