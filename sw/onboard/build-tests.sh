#!/bin/bash

OK=0
FILES=`ls test_*_main.c`

for f in $FILES
do
	t=`echo $f | sed -e 's/\.c//'`
	echo "BUILDING $t"
	make TARGET=$t > /dev/null
	if [ $? -eq 0 ] ; then
		echo "    [OK]"
    else
        OK=1
	fi
done

exit $OK
