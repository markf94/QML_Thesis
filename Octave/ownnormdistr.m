
%global sigma = 1
%global mu = 0

% Define function for normal distribution
function y = f (x)
%global sigma
%global mu
%sigma = 1
%mu = 0
y = 1/(1 .* sqrt(2 .*pi)).*exp(-(x).^2/(2));
%y = 1/(sigma .* sqrt(2 .*pi)).*exp(-(x-mu).^2/(2.*sigma.^2));
endfunction
%x=[-4:0.1:4];
%for i=0:3
myprob = f(1)
%endfor
%plot(x,myprob)