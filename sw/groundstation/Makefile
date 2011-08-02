ME=$(shell pwd | sed -e 's/\//\\\//g')
DFILE="groundstation.desktop"
ICON="groundstation.svg"

test:
	@PYTHONPATH=. find wasp/test/ -name 'test*.py' -exec python {} \;
	@PYTHONPATH=. find gs/test/ -name 'test*.py' -exec python {} \;

clean:
	@find . -name '*.pyc' -exec rm -f {} \;

install-local:
	@echo "Installing .desktop file in "$(HOME)"/.local/share/applications/"$(DFILE)
	@cat $(DFILE) | sed -e "s/Exec=/Exec=$(ME)\//g" > $(HOME)/.local/share/applications/$(DFILE)
	@cp -f ./data/icons/rocket.svg $(HOME)/.local/share/icons/$(ICON)

uninstall-local:
	@echo "Removing .desktop file from "$(HOME)"/.local/share/applications/"$(DFILE)
	@rm -f $(HOME)/.local/share/applications/$(DFILE)
	@rm -f $(HOME)/.local/share/icons/$(ICON)

