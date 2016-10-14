

%3/4 state
a = 0.85355 - 0.35355i
b = 0.35355 - 0.14645i
1/4*(((a+1)*conj(a+1))^2+((a)*conj(a))^2+((b)*conj(b))^2+((b+1)*conj(b+1))^2)
1-1/4*(((a-1)*conj(a-1))^2+((a)*conj(a))^2+((b)*conj(b))^2+((b-1)*conj(b-1))^2)
%this one yields the right prediction:
1/8*(abs(a+1)^2+abs(a)^2+abs(b)^2+abs(b+1)^2)

%7/8 state
a = 0.96194 - 0.19134i
b = 0.19134 - 0.03806i
1/4*(((a+1)*conj(a+1))^2+((a)*conj(a))^2+((b)*conj(b))^2+((b+1)*conj(b+1))^2)
1-1/4*(((a-1)*conj(a-1))^2+((a)*conj(a))^2+((b)*conj(b))^2+((b-1)*conj(b-1))^2)
%this one yields the right prediction:
1/8*(abs(a+1)^2+abs(a)^2+abs(b)^2+abs(b+1)^2)
1-1/8*(abs(a-1)^2+abs(a)^2+abs(b)^2+abs(b-1)^2)

%Binary classifier in x-y plane
atil = 0.70711
btil =  0.50000 + 0.50000i
a0 =  0.70711
b0 =  0.00000 + 0.70711i
a1 =  0.70711
b1 = -0.00000 - 0.70711i
1/4*(abs(atil+a0)^2+abs(atil+a1)^2+abs(btil+b0)^2+abs(btil+b1)^2)
1-1/4*(abs(atil-a0)^2+abs(atil-a1)^2+abs(btil-b0)^2+abs(btil-b1)^2)
1/8*(abs(atil+a0)^2+abs(atil+a1)^2+abs(btil+b0)^2+abs(btil+b1)^2)
1-1/8*(abs(atil-a0)^2+abs(atil-a1)^2+abs(btil-b0)^2+abs(btil-b1)^2)
