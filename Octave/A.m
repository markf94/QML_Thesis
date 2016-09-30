function A = computeAmatrix(theta_z, theta_y)
  R_z = [exp(-i*theta_z/2) 0; 0 exp(i*theta_z/2)];
  R_y = [cos(theta_y/2) -sin(theta_y/2); sin(theta_y/2) cos(theta_y/2)];
  A = R_z*R_y;
endfunction