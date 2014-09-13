function [a, b] = trig_poly(x,m)
% approximate or interpolate n data points
% at t=0, 2pi/n,...,2k pi/n,...,2(n-1)pi/n
% use trigonometric polynomila of degree m, with
%       2m + 1 < n           for appriximation
%       2m + 1 = n or 2m = n for interpolation
n = length(x);
w = 2*pi/n;
t = 0: w : (2*pi - w); t = t';
a = zeros(m ,1);
b = a;

% find coefficients (summation included in vector product)
for j = 1 : m
    a(j) = x*cos(j*t);
    b(j) = x*sin(j*t);
end

a = 2*a/n;
b = 2*b/n;

a0 = sum(x)/n;
if (n == 2*m)
    a(m) = a(m)/2;
end

%evaluate trig polynomial on [0, 2*pi]
tt = 0 : 0.1 : 2*pi;
xx = a0 + a(1)*cos(tt) + b(1)*sin(tt);

for j = 2 :m
    xx = xx + a(j)*cos(j*tt) + b(j)*sin(j*tt);
end

%plot function and data:
figure(1)
title('DFT of the sequence');
plot(tt, xx, t, x, '*')
grid on
% display coefficients
a,b