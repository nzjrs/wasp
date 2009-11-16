%Rocket motor calculations
%
%Optimisation of solid fuel rocket motor using RNX-57V propellent
%
%Author: Malcolm Snowdon
%Date: 9th June 2009
%Updated 7th August 2009

% clear;
% clc;

%--------------------------Variables---------------------------------------
p0 = 3.1e6; %Chamber pressure (MPa), S3
pe = 101.325e3; %Exit pressure (KPa)
T0 = 2000; %Champer temperature (K)****************************************

t = 0.0014; %Wall thickness (m)
Di = 0.0605; %Inner diameter (m)
L_Grain = 0.1; %Propellent segment length (m)
t_Grain = 0.02; %Propellent wall thickness (m)
Ds = 0.005; %Cap screw diameter
N_Screws = 8; %Number of cap screws in nozzel or balkhead
S_Yield = 350e6; %Yield stress (MPa), 304 stainless
Tor_Yield = 500e6; %Shear strength of cap screws (check value)*************
N_Segments = 4; %Number of propellent segments

k = 1.055; %Ratio of specific heats
R = 287; %J/kg assuming same as air****************************************

[A_max,mass_Grain] = Fuel_Grain(Di,L_Grain,t_Grain);
Burn_Area = A_max*N_Segments;%0.01656; %Burn surface area (m^2)
mass = mass_Grain*N_Segments; %Mass of propellent

%-------------------------Casing Stresses----------------------------------

%Hoop stress
S_Hoop = p0*Di/2/t; %Assuming thin wall, S1

%Longitudinal stress
S_Long = p0*Di^2/((Di+2*t)^2-Di^2); %S2

%von Mises, pg 121 Boresi and Schmidt
S_e = sqrt(1/2*((S_Hoop-S_Long)^2 + (S_Long - p0)^2 + (p0 - S_Hoop)^2));

SF = S_Yield/S_e; %Distortion energy safety factor
fprintf('\nCasing Safety Factor SF = %f\n',SF);

%Shear on cap screws

Tor_Screw = p0*Di^2/Ds^2/N_Screws;
SF_Screw = Tor_Yield/Tor_Screw;
fprintf('Cap Screw Safety Factor = %f\n',SF_Screw);

%Compression around holes
S_Holes = p0*pi/4*Di^2/Ds/t/N_Screws;
SF_Holes = S_Yield/S_Holes;
fprintf('Hole Safety Factor SF = %f\n',SF_Holes);

%---------------------Nozzle Geometry--------------------------------------

% Kn = 272*(p0/1e6)^0.641; %From Nakka's RNX-71V plot
% 
% %Expansion ratio A*/Ae
% A_Ratio = ((k+1)/2)^(1/(k-1))*(pe/p0)^(1/k)*sqrt((k+1)/(k-1)*(1-(pe/p0)^((k-1)/k)));
% A_Star = Burn_Area/Kn;
% A_e = A_Star/A_Ratio;
% D_Throat = sqrt(4*A_Star/pi);
% D_Exit =  sqrt(4*A_e/pi);
fprintf('D_Throat = %.2f, D_Exit = %.2f (mm)\n',D_Throat*1000,D_Exit*1000);

%--------------------Performance-------------------------------------------
%Thrust
F = A_Star*p0*sqrt(2*k^2/(k-1)*(2/(k+1))^((k+1)/(k-1))*(1-(pe/p0)^((k-1)/k)));
fprintf('Thrust = %fN\n',F);

m_dot = p0*A_Star*sqrt(k/R/T0)*((k+1)/2)^((k+1)/2/(1-k)); %Mass flow rate
Burn_Time = mass/m_dot;
fprintf('Burn Time = %f seconds\n',Burn_Time);