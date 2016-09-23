%% Permuting the initial condition

counter = 1
for a = 0:(pi/4):(3/2*pi)
  for b = 0:(pi/4):(3/2*pi)
    for c = 0:(pi/4):(3/2*pi)
      for d = 0:(pi/4):(3/2*pi)
        [x, info] = fsolve (@f, [a;b;c;d], optimset ("MaxIter" , 10000))
        if (round(imag(x)) == [0;0;0;0])
          save_solution(counter,1:4) = x'
          counter = counter+1
        endif
      endfor
    endfor
  endfor
endfor

