function C = computeCmatrix(alpha, beta, gamma, delta)
  theta_z = (delta-beta)/2;
  R_z = [exp(-i*theta_z/2) 0; 0 exp(i*theta_z/2)];
  %R_y = [cos(theta_y/2) -sin(theta_y/2); sin(theta_y/2) cos(theta_y/2)];
  C = R_z;
endfunction