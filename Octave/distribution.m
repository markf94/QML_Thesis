%% Sample points from a given distribution

%% Using only log-concave probability distributions

%RD = poissrnd(7,10,10);
RD = random("poisson", 10, [50, 50]);
%RD = random("normal", 5,2, [50, 50]);
hist (RD, 100);
colormap (summer ());
