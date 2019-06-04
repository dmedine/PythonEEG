
%%
[b,a] = butter(5, [8/125,14/125],'bandpass');
data = ones(1,256);
freq = 10;
per = 250/freq

for n=0:length(data)/per-1
    data(n*per+1) = -1;
end
    
%%
data = zeros(1,256);
data(1)=1;
%%
x=data;
[y0,z] = filter(b,a,x(1:64));
[y1, z] = filter(b,a,x(65:128),z);
[y2, z] = filter(b,a,x(129:192),z);
[y3, z] = filter(b,a,x(193:256),z);
y = [y0,y1,y2,y3];
%% 
cd C:\\Users\\David.Medine\\Desktop
%%
streams = load_xdf('test.xdf');
streams{1}.info.name
streams{2}.info.name

%%
figure
plot(streams{1}.time_series')
%%
figure
plot(streams{2}.time_series')


%%
figure
plot(streams{1}.time_stamps, streams{1}.time_series')
hold
plot(streams{2}.time_stamps, streams{2}.time_series')

%%
figure;
plot(y)
hold
plot(x)
Y = fft(y)/256;
X = fft(x)/256;
figure;
freqs = linspace(0,250-250/256,256);
plot(freqs(1:129),20*log(abs(Y(1:129))));
hold
plot(freqs(1:129), 20*log(abs(X(1:129))));

    
    