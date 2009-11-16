clear
% load data

time=0:0.1:60;
time_theta5=0:0.1:120;
tt=0:0.001:60;

% plot the sequence of changes to RPM and thruster angle

% RPMa is thruster angle=7.5
% RPM is thruster angle=12.5
% RPMb is thruster angle=17.5
for n=1:4
    load(strcat('\r_RPM',num2str(n)))
    load(strcat('\v_RPM',num2str(n)))
    r=interp1(time,r,tt);
    v=interp1(time,v,tt);
    r_RPM{n}=r; v_RPM{n}=v;
    load(strcat('\ra_RPM',num2str(n)))
    load(strcat('\va_RPM',num2str(n)))
    r=interp1(time,r,tt);
    v=interp1(time,v,tt);
    r_RPMa{n}=r; v_RPMa{n}=v;    
    load(strcat('\rb_RPM',num2str(n)))
    load(strcat('\vb_RPM',num2str(n)))
    r=interp1(time,r,tt);
    v=interp1(time,v,tt);
    r_RPMb{n}=r; v_RPMb{n}=v;    
end

time=tt;

% plot the sequence of changes to RPM and thruster angle
% figure(1); subplot(2,1,1); plot(time,r_RPM{1},'b',time+60,r_RPM{2},'b',time+120,r_RPM{3},'b',time+180,r_RPM{4},'b'); ylabel('r(t)'); title('changes in RPM');
% subplot(2,1,2); plot(time,v_RPM{1},'b',time+60,v_RPM{2},'b',time+120,v_RPM{3},'b',time+180,v_RPM{4},'b'); xlabel('t'); ylabel('v(t)');


RPM=[700+875,700+2*875,700+3*875,700+4*875]';
theta=[12.5-5,12.5,12.5+5];

delta=0.05;

for n=1:4
    r=r_RPM{n}; v=v_RPM{n};
    r=(1+delta*randn(1,length(time))).*(1+delta/2*(sin(20*time)+sin(2*pi*time).^3)).*r;
    v=(1+delta*randn(1,length(time))).*(1+delta/2*(sin(20*time)+sin(2*pi*time).^3)).*v;
    r=r'; v=v';
    %rss1=r(end); vss1=v(end);
    
    % obtain steady state from the mean of data after 3 seconds
    rss1=mean(r(30000:end)); vss1=mean(v(30000:end));
    
    % compute the initial condition, by computing a least squares straight
    % line through first 0.5 seconds
    [P1,S]=polyfit(time(1:500),r(1:500)',1);
    [P2,S]=polyfit(time(1:500),v(1:500)',1);
    r0=P1(2); v0=P2(2);
    %r0=r(1); v0=v(1);
    A1=[cumtrapz(time,r-rss1),cumtrapz(time,v-vss1)]; q1=r-r0; q2=v-v0;
    A1b=[cumtrapz(time,r-rss1)];
    soln1=A1b\q1;
    soln2=A1\q2;
    a11_RPM(n)=soln1(1); a12_RPM(n)=0;%soln1(2);
    a21_RPM(n)=soln2(1); a22_RPM(n)=soln2(2);
    b1_RPM(n)=-a11_RPM(n)*rss1-a12_RPM(n)*vss1;
    b2_RPM(n)=-a21_RPM(n)*rss1-a22_RPM(n)*vss1;
    r0_RPM(n)=r0; v0_RPM(n)=v0;
end

for n=1:4
    r=r_RPMa{n}; v=v_RPMa{n};
    r=(1+delta*randn(1,length(time))).*(1+delta/2*(sin(20*time)+sin(2*pi*time).^3)).*r;
    v=(1+delta*randn(1,length(time))).*(1+delta/2*(sin(20*time)+sin(2*pi*time).^3)).*v;
    r=r'; v=v';    
    %rss1=r(end); vss1=v(end);
    %r0=r(1); v0=v(1);
    rss1=mean(r(30000:end)); vss1=mean(v(30000:end));
    [P1,S]=polyfit(time(1:500),r(1:500)',1);
    [P2,S]=polyfit(time(1:500),v(1:500)',1);
    r0=P1(2); v0=P2(2);
    A1=[cumtrapz(time,r-rss1),cumtrapz(time,v-vss1)]; q1=r-r0; q2=v-v0;
    A1b=[cumtrapz(time,r-rss1)];
    soln1=A1b\q1;
    soln2=A1\q2;
    a11_RPMa(n)=soln1(1); a12_RPMa(n)=0;%soln1(2);
    a21_RPMa(n)=soln2(1); a22_RPMa(n)=soln2(2);
    b1_RPMa(n)=-a11_RPMa(n)*rss1-a12_RPMa(n)*vss1;
    b2_RPMa(n)=-a21_RPMa(n)*rss1-a22_RPMa(n)*vss1;
    r0_RPMa(n)=r0; v0_RPMa(n)=v0;
end

for n=1:4
    r=r_RPMb{n}; v=v_RPMb{n};
    r=(1+delta*randn(1,length(time))).*(1+delta/2*(sin(20*time)+sin(2*pi*time).^3)).*r;
    v=(1+delta*randn(1,length(time))).*(1+delta/2*(sin(20*time)+sin(2*pi*time).^3)).*v;
    r=r'; v=v';
    %rss1=r(end); vss1=v(end);
    %r0=r(1); v0=v(1);
    rss1=mean(r(30000:end)); vss1=mean(v(30000:end));
    [P1,S]=polyfit(time(1:500),r(1:500)',1);
    [P2,S]=polyfit(time(1:500),v(1:500)',1);
    r0=P1(2); v0=P2(2);
    A1=[cumtrapz(time,r-rss1),cumtrapz(time,v-vss1)]; q1=r-r0; q2=v-v0;
    A1b=[cumtrapz(time,r-rss1)];
    soln1=A1b\q1;
    soln2=A1\q2;
    a11_RPMb(n)=soln1(1); a12_RPMb(n)=0;%soln1(2);
    a21_RPMb(n)=soln2(1); a22_RPMb(n)=soln2(2);
    b1_RPMb(n)=-a11_RPMb(n)*rss1-a12_RPMb(n)*vss1;
    b2_RPMb(n)=-a21_RPMb(n)*rss1-a22_RPMb(n)*vss1;
    r0_RPMb(n)=r0; v0_RPMb(n)=v0;
end


% compute a 2nd order model for relating coefficients
theta1=[12.5-5,12.5-5,12.5-5,12.5-5]';
theta2=[12.5,12.5,12.5,12.5]';
theta3=[12.5+5,12.5+5,12.5+5,12.5+5]';
X1=[RPM.^0, theta1, RPM, RPM.^2, theta1.*RPM, theta1.^2, theta1.*RPM.^2, theta1.^2.*RPM.^2];
X2=[RPM.^0, theta2, RPM, RPM.^2, theta2.*RPM, theta2.^2, theta2.*RPM.^2, theta2.^2.*RPM.^2];
X3=[RPM.^0, theta3, RPM, RPM.^2, theta3.*RPM, theta3.^2, theta3.*RPM.^2, theta3.^2.*RPM.^2];

AA=[X1; X2; X3]; bb=[b1_RPMa, b1_RPM, b1_RPMb]';
soln=AA\bb;
AA2=[X1; X2; X3]; bb2=[b2_RPMa, b2_RPM, b2_RPMb]';
soln2=AA2\bb2;
AA3=[X1; X2; X3]; bb3=[a11_RPMa, a11_RPM, a11_RPMb]';
soln3=AA3\bb3;
AA4=[X1; X2; X3]; bb4=[a21_RPMa, a21_RPM, a21_RPMb]';
soln4=AA4\bb4;
AA5=[X1; X2; X3]; bb5=[a22_RPMa, a22_RPM, a22_RPMb]';
soln5=AA5\bb5;



B1=AA*soln;
B2=AA2*soln2;
A11=AA3*soln3;
A21=AA4*soln4;
A22=AA5*soln5;

[B1,[b1_RPMa';b1_RPM';b1_RPMb']];
[B2,[b2_RPMa';b2_RPM';b2_RPMb']];

X1_true=[b1_RPMa';b1_RPM';b1_RPMb'];
X2_true=[b2_RPMa';b2_RPM';b2_RPMb'];

b1_RPMa=B1(1:4); b1_RPM=B1(5:8); b1_RPMb=B1(9:12);
b2_RPMa=B2(1:4); b2_RPM=B2(5:8); b2_RPMb=B2(9:12);
a11_RPMa=A11(1:4); a11_RPM=A11(5:8); a11_RPMb=A11(9:12);
a21_RPMa=A21(1:4); a21_RPM=A21(5:8); a21_RPMb=A21(9:12);
a22_RPMa=A22(1:4); a22_RPM=A22(5:8); a22_RPMb=A22(9:12);

[mean(abs((X1_true-B1)./X1_true)),mean(abs((X2_true-B2)./X2_true))];


%RPM=[700+875,700+2*875,700+3*875,700+4*875]';
RPM=[1800,2500,2000,3000]';
theta=(12.5)*RPM.^0;

NN=length(RPM);

X=[RPM.^0, theta, RPM, RPM.^2, theta.*RPM, theta.^2, theta.*RPM.^2, theta.^2.*RPM.^2];

B1=X*soln;
B2=X*soln2;
A11=X*soln3;
A21=X*soln4;
A22=X*soln5;

r0=-8.5538; v0=0.7954;

tspan=[0,0];
R=r0;
V=v0;
T=0;
for nn=1:NN
    tspan=[tspan(2),tspan(2)+60];
    b1=B1(nn); b2=B2(nn);
    a11=A11(nn); a12=0; a21=A21(nn); a22=A22(nn);
    options=odeset('MaxStep',0.1);
    soln=ode45(@linear_model,tspan,[r0 v0],options,a11,a12,a21,a22,b1,b2);
    tt=tspan(1):0.1:tspan(2);
    Y=deval(soln,tt);
    r_sim=Y(1,:);
    v_sim=Y(2,:);
    R=[R,r_sim(2:end)];
    V=[V,v_sim(2:end)];
    T=[T,tt(2:end)];
    r0=R(end); v0=V(end);
end

%T=0:0.1:240;
figure(1); plot(T,R,'g',time,r_RPM{1},'b',time+60,r_RPM{2},'b',time+120,r_RPM{3},'b',time+180,r_RPM{4},'b');
figure(2); plot(T,V,'g',time,v_RPM{1},'b',time+60,v_RPM{2},'b',time+120,v_RPM{3},'b',time+180,v_RPM{4},'b');



