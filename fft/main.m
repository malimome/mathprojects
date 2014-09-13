%include fft.m
%include trig_poly.m
%This is DFT
z = [1 1 1 1 0 0 0 0];
trig_poly(z, 4)

%Here is FFT, test different vectors
z = [1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ];
z = [1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 ];
n = length(z);
ans = fft(z)
a = zeros(1, n/2);
b = zeros(1, n/2);
tt = 0 : 0.01 : 2*pi;
a0 = real(ans(1))/n;
yy = a0;
for i = 1 : n/2
    a(i) = 2 * real(ans(i+1))/n;
    b(i) = -2 * imag(ans(i+1))/n;
    yy = yy + a(i)*cos(i*tt) + b(i)*sin(i*tt);
end
yy = yy + cos(tt*(n/2))*2*real(ans(n/2+1))/n;
t = 0 : 2*pi/n : (2*pi-pi/n);
figure(2)
title('fft of the sequence');
plot(tt, yy, t, z, '*')
grid on
a,b