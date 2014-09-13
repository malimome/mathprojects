function y = FFT(x) 

    n=length(x);
    g = exp(2*pi*i/n);
    if (n==1) return x;
    m = n/2;
    for j = 0 : m-1
        X = x(2j);
        Y = x(2j+1);
    end
    X = FFT(X);
    Y = FFT(Y);
    for k = 0 : n-1
        U[k] = X(k mod m);
        V[k] = g^(-k)*Y(k mod m);
    end
    return U+V;
