ME = $(shell pwd | sed -e 's/\//\\\//g')
DFILE = "groundstation.desktop"

test:
	@PYTHONPATH=. find wasp/test/ -name 'test*.py' -exec python {} \;
	@PYTHONPATH=. find gs/test/ -name 'test*.py' -exec python {} \;

clean:
	@find . -name '*.pyc' -exec rm -f {} \;

install:
	@echo "Installing .desktop file in "$(HOME)"/.local/share/applications/"$(DFILE)
	@cat $(DFILE) | sed -e "s/Exec=/Exec=$(ME)\//g" -e 's/Icon=groundstation/Icon=$(ME)\/data\/icons\/rocket.svg/g' > $(HOME)/.local/share/applications/$(DFILE)

uninstall:
	@echo "Removing .desktop file from "$(HOME)"/.local/share/applications/"$(DFILE)
	@rm -f $(HOME)/.local/share/applications/$(DFILE)

.PHONY: test
