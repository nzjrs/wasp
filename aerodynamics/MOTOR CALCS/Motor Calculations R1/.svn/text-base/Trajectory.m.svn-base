%Numerical trajectory calculation

clear;
% clc;

Cd = .75; %Drag Coefficient
rho = 1.2; %Air density (kg/m^3)
A = pi*0.087^2/4; %Presented area (m^2)

dt = 0.1; %Time increment (s)
t_sim = 70; %Duration of simulation (s)
t_burn = 3.5; %Burn time (s)
prop_mass = 1.6; %Propellent mass (kg)
dry_mass = 4.8; %Unfuelled mass incl. motor casing (kg)

N = t_sim/dt; %Number of iterations

F_motor = 336; %Motor thrust (N)
F = [F_motor*ones(1,t_burn/dt),zeros(1,N-t_burn/dt)]; %Array of thrust force (N)
F_total = zeros(1,N); %Total force (thrust - drag - gravity) (N)
mass = [linspace(prop_mass+dry_mass,dry_mass,t_burn/dt),dry_mass*ones(1,N-t_burn/dt)]; %Mass array (kg)
U = zeros(1,N+1); %Velocity (m/s)
F_aero = zeros(1,N); %Aerodynamic drag

for i = 1:N
    F_aero(i) = 1/2*Cd*rho*A*U(i)^2*sign(U(i));
    F_total(i) = F(i) - F_aero(i) - 9.81*mass(i); %Thrust - aerodynamic drag - mg
    U(i+1) = U(i) + F_total(i)/mass(i)*dt; %New velocity (by Newton's method?)
end

h = dt*cumtrapz(U); %Ascent height (m) by numerical integration of velocity

% figure(1);plot(0:dt:N*dt,U,0:dt:N*dt,h/10);xlabel('Time (s)');
% legend('Velocity (m/s)','Height/10 (m)');grid on;

fprintf('Max velocity = %.1f m/s, max height = %.1f m\n',max(U),max(h));

figure(2);plot(0:dt:N*dt-dt,F_total,0:dt:N*dt-dt,F,0:dt:N*dt-dt,-F_aero,...
    0:dt:N*dt-dt,mass*100,0:dt:N*dt,h/20,0:dt:N*dt,U);
xlabel('Time (s)');grid on;
legend('Total Force','Thrust','Drag Force','Mass x 100','Height / 20','Velocity');

