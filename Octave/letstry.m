function [A, B, C, alpha, beta, gamma, delta] = letstry(U)
  %Compute beta and delta first
  

  %% MIGHT NEED TO ADJUST THE STARTING VALUES OF FSOLVE!
  [x, info] = fsolve (@f, [pi,pi]);
  %correcting for imaginary round off error
  global beta = real(x(1));
  global delta = real(x(2));
  
  
endfunction