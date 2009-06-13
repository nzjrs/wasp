#!/bin/sh

PPZ_BRANCH=wasp-gps
PPZ_DIR=/home/john/Programming/paparazzi.git/
WASP_DIR=/home/john/Programming/wasp/

PPZ_SW_DIR=$PPZ_DIR/wasp/src
WASP_SW_DIR=$WASP_DIR/sw/onboard

PPZ_MESSAGES=$PPZ_DIR/wasp/messages.xml
WASP_MESSAGES=$WASP_DIR/sw/messages.xml

PPZ_TOOLS_DIR=$PPZ_DIR/wasp/tools
WASP_TOOLS_DIR=$WASP_DIR/sw/tools

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

	echo "COPYING MESSAGES  FROM $PPZ_MESSAGES to $WASP_MESSAGES"
	rsync								\
		--verbose						\
		--update						\
		$PPZ_MESSAGES $WASP_MESSAGES

	echo "COPYING TOOLS FROM $PPZ_TOOLS_DIR/ to $WASP_TOOLS_DIR/"
 	rsync								\
		--archive						\
		--verbose						\
		--cvs-exclude					\
		--exclude='*.pyc'				\
		$PPZ_TOOLS_DIR/ $WASP_TOOLS_DIR/
else
	echo "INCORRECT BRANCH $BRANCH"
fi

