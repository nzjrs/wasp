%RNX propellant mixture
clear;
clc;

n_hardener = 0.034;
n_resin = 0.206;
n_rust = 0.08;
n_nitrate = 0.68;

n_hardener + n_resin + n_rust + n_nitrate;

mass = 1700;

fprintf('\nRNX-71V PROPORTIONS\n\nHardener:\t%.2f g\nResin:\t\t%.2f g\nNitrate:\t%.2f g\nFe302:\t\t%.2f g\n',...
    mass*n_hardener,mass*n_resin,mass*n_nitrate,mass*n_rust);
fprintf('\nTotal mass: %.2f g\n',mass);
