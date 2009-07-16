#!/bin/sh

PPZ_BRANCH=wasp
PPZ_DIR=/home/john/Programming/paparazzi.gitsvn/
WASP_DIR=/home/john/Programming/wasp.git/

PPZ_SW_DIR=$PPZ_DIR/wasp/src
WASP_SW_DIR=$WASP_DIR/sw/onboard

PPZ_TOOLS_DIR=$PPZ_DIR/wasp/tools
WASP_TOOLS_DIR=$WASP_DIR/sw/tools

PPZ_MESSAGES_DOT_PY=$PPZ_TOOLS_DIR/messages.py
WASP_MESSAGES_DOT_PY=$WASP_DIR/sw/groundstation/wasp/messages.py

PPZ_SETTINGS_DOT_PY=$PPZ_TOOLS_DIR/settings.py
WASP_SETTINGS_DOT_PY=$WASP_DIR/sw/groundstation/wasp/settings.py

#make sure that we are copying code from the correct wasp branch
BRANCH=`GIT_DIR=$PPZ_DIR/.git git symbolic-ref HEAD | cut -d / -f 3`
if [ $BRANCH = $PPZ_BRANCH ]
then
	echo "COPYING CODE FROM $PPZ_SW_DIR/ to $WASP_SW_DIR/"
 	rsync								\
		--archive						\
		--verbose						\
		--cvs-exclude					\
		--exclude='/bin*'				\
		--exclude='/generated*' 		\
		$PPZ_SW_DIR/ $WASP_SW_DIR/

	echo "COPYING TOOLS FROM $PPZ_TOOLS_DIR/ to $WASP_TOOLS_DIR/"
 	rsync								\
		--archive						\
		--verbose						\
		--cvs-exclude					\
		--exclude='*.pyc'				\
		--exclude='messages.py'			\
		--exclude='settings.py'			\
		$PPZ_TOOLS_DIR/ $WASP_TOOLS_DIR/

	echo "COPYING MESSAGES.py FROM $PPZ_MESSAGES_DOT_PY to $WASP_MESSAGES_DOT_PY"
	rsync								\
		--verbose						\
        $PPZ_MESSAGES_DOT_PY $WASP_MESSAGES_DOT_PY

	echo "COPYING SETTINGS.py FROM $PPZ_SETTINGS_DOT_PY to $WASP_SETTINGS_DOT_PY"
	rsync								\
		--verbose						\
        $PPZ_SETTINGS_DOT_PY $WASP_SETTINGS_DOT_PY

    #now commit here with the same message
    COMMIT_FILE=`mktemp`
    GIT_DIR=$PPZ_DIR/.git git log --pretty=format:"%b%s" -1 > $COMMIT_FILE
    git commit -a -F $COMMIT_FILE -e
else
	echo "INCORRECT BRANCH $BRANCH"
fi

