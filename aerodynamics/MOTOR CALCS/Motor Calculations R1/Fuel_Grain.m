function [A_max,mass] = Fuel_Grain(OD,L,a0)
%Fuel Grain burn surface area


%Sample Output:
%for r = 38mm, a0 = 14mm, b0 = 45mm:
%Average burn surface: 0.0036788 m^2
%Slightly decreasing area

N = 100;
density = 1664; %Density of RNX-71V (kg/m^3)
r = OD/2;%outer diameter(constant)***************0.5mm insulation
% a0 = t/;%Initial wall thickness
b0 = L;%Initial cylinder height
d = linspace(0,a0,N);
%d is the distance burned into the propellent surface

for i = 1:N
    a = a0 - d(i);
    b = b0 - 2*d(i);
    A(i) = 4*pi*a*r - 2*pi*a^2 + 2*pi*r*b - 2*pi*a*b;
    Aa(i) = 4*pi*a*r - 2*pi*a^2;
    Ab(i) = 2*pi*r*b - 2*pi*a*b;
end

plot(d,A,d,Aa,d,Ab)
grid on;
legend('Total Area','A end','A core','location','southeast')

A_max = max(A);
% disp(['Average burn surface: ' num2str(mean(A)) ' m^2'])
% disp(['Max burn surface: ' num2str(A_max) ' m^2'])
mass = density*pi/4*(OD^2-(OD-2*a0)^2)*L;
