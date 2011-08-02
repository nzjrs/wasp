all: www/images/logo.png www/index.html www/style/default.css
	-rsync -av www/ root@greenbirdsystems.com:/var/www/waspuav.org/

www/images/logo.png: logo.svg
	-inkscape --export-png=$@ --export-width=256 --export-height=60 $<
