#!/bin/bash

OK=0
FILES=`ls test/test_*_main.c`
FILES="$FILES autopilot_main.c"
ARCHES=`ls arch/Makefile.* | cut -d. -f2`

for a in $ARCHES
do
    rm -rf bin/$a
    for f in $FILES
    do
	    t=`echo $f | sed -e 's/\.c//'`
	    echo -e "[$a]\tBUILDING $t"
	    make TARGET=$t ARCH=$a > /dev/null
	    if [ $? -eq 0 ] ; then
            size=`make TARGET=$t size | grep Total | cut --delimiter=" " -f 14`
		    echo -e "\t[OK] (size: ${size}b)"
        else
            OK=1
	    fi
    done
done

exit $OK
