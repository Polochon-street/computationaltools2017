#!/bin/sh

awk 'BEGIN{ print "Verifying that fields 2 and 3 are numbers"; FS="|"}
$2 !~/^[0-9].[0-9]*$/ { print "Error in the first field, number expected (line "NR"):\n" $0}
$3 !~/^[0-9].[0-9]*$/ { print "Error in the second field, number expected (line "NR"): \n" $0}
END { print "Finished verification"} ' data_file

awk 'BEGIN { print "Looking for lines where the third field is < 0.1 and exping them:"; FS="|" }
$3 < 0.1 { print exp($3) }
END { print "Finished computation"} ' data_file
