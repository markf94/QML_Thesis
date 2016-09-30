%% SCRIPT FOR CREATING A CONTROLLED-U QUANTUM GATE

% THEOREM:
% For any unitary matrix U we can find a decomposition into A,B,C such that:
% A*B*C = I
% exp(i*alpha)*A*X*B*X*C = U
% where X is the first Pauli matrix (NOT gate) and alpha is some real number
% The circuit goes C > CNOT > B > CNOT > A

%% Function that computes ABC decomposition of any unitary matrix U:

%function [A, B, C, alpha, beta, gamma, delta] = decompose(U)
  
  %Compute beta and delta first
  function y = f(x)
  global U
  %x(1) is beta
  %x(2) is delta
  y(1) = exp(i*(x(1)+x(2)))-U(2,2)/U(1,1);
  y(2) = exp(i*(x(1)-x(2)))+U(2,1)/U(1,2);
  endfunction

  %% MIGHT NEED TO ADJUST THE STARTING VALUES OF FSOLVE!
  [x, info] = fsolve (@f, [pi,pi]);
  %correcting for imaginary round off error
  global beta = real(x(1));
  global delta = real(x(2));
  
  %Compute gamma
  function y = f(x)
  global delta
  global U
  %x(1) is gamma
  %y(1) = cos(x(1)/2)+sin(x(1)/2)*exp(delta)*(-U(1,1)/U(1,2))
  y(1) = U(2,2)*exp(-i*delta)*tan(x(1)/2)-U(2,1)
  endfunction
  
  %% MIGHT NEED TO ADJUST THE STARTING VALUES OF FSOLVE!
  %not 100% sure about this one!
  [x, info] = fsolve (@f, [0]);
  global gamma = real(x);
  
  % Finally, find alpha
  function y = f(x)
  global beta
  global delta
  global gamma
  global U
  %x(1) is alpha
  y(1) = U(2,2)*exp(-i*(beta/2+delta/2))*1/(cos(gamma/2))-exp(i*x(1))
  endfunction

  %% MIGHT NEED TO ADJUST THE STARTING VALUES OF FSOLVE!
  [x, info] = fsolve (@f, [pi]);
  global alpha = real(x);

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
%endfunction