ME = $(shell pwd | sed -e 's/\//\\\//g')
DFILE = "groundstation.desktop"

test:
	@PYTHONPATH=. python wasp/test/test.py
	@PYTHONPATH=. python wasp/test/test_ui.py

clean:
	@rm -rf wasp/test/html/

install:
	@echo "Installing .desktop file in "$(HOME)"/.local/share/applications/"$(DFILE)
	@cat $(DFILE) | sed -e "s/Exec=/Exec=$(ME)\//g" -e 's/Icon=groundstation/Icon=$(ME)\/gs\/ui\/icons\/rocket.svg/g' > $(HOME)/.local/share/applications/$(DFILE)

uninstall:
	@echo "Removing .desktop file from "$(HOME)"/.local/share/applications/"$(DFILE)
	@rm -f $(HOME)/.local/share/applications/$(DFILE)

.PHONY: test
