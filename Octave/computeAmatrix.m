function A = computeAmatrix(alpha, beta, gamma)
  theta_z = beta;
  theta_y = gamma/2;
  R_z = [exp(-i*theta_z/2) 0; 0 exp(i*theta_z/2)];
  R_y = [cos(theta_y/2) -sin(theta_y/2); sin(theta_y/2) cos(theta_y/2)];
  A = R_z*R_y;
endfunction