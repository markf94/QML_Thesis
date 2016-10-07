%Project a two-level qubit state onto Bloch sphere

function [x,y,z,theta,phi] = bloch(alpha, beta)
% INPUT
% alpha|0> + beta|1>
% a and b are probability amplitudes from qubit

% Find and eliminate global phase
angle_alpha = angle(alpha)
angle_beta = angle(beta)
if angle_alpha > angle_beta
alpha_new = alpha/exp(i*angle_beta)
beta_new = beta/exp(i*angle_beta)
else
alpha_new = alpha/exp(i*angle_alpha)
beta_new = beta/exp(i*angle_alpha)
endif

%Computing theta and phi from probability amplitudes
theta = 2*acos(alpha_new);
phi = -i*log(beta_new/sin(theta/2));

%Theta and phi
%polar to cartesian conversion

%disp("============================")
%disp("x,y,z with imaginary part")
%x = sin(abs(theta))*cos(abs(phi));
x = sin(theta)*cos(phi);
%y = sin(abs(theta))*sin(abs(phi));
y = sin(theta)*sin(phi);
%z = cos(abs(theta));
z = cos(theta);
disp("============================")

disp("Check for vector length one...")
r = round(sqrt(x^2+y^2+z^2)*10)/10
if (round(sqrt(x^2+y^2+z^2)*10)/10==1)
disp("ok")
disp("============================")
endif

endfunction