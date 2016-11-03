x=[-4:0.1:4];
plot (x,normpdf(x,0,1));
print -dpng "-S400,400" normal.png