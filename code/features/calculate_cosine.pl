#!/usr/bin/perl
#
#  Author: Preslav Nakov
#  
#  Description: Calculates cosine vectors between a question and an answer.
#
#  Last modified: July 9, 2016
#
#

use warnings;
use strict;
use utf8;

################
###   MAIN   ###
################

die "One argument expected:" if (0 != $#ARGV);
my $VECTORS_FILE_NAME = $ARGV[0];

### 1. Fetch the vectors file
my @qVect = ();
my $qID = ();
open(VECTORS, $VECTORS_FILE_NAME) or die "Failed to open $VECTORS_FILE_NAME";
while (<VECTORS>) {

   ### 1. Check the file format and get the vector
	die "Wrong file format!" if (!/^(Q\d+[^\t]*)\t([^\n\r]+)[\n\r]*$/);
   my ($id, $vect) = ($1, $2);

   ### 2. If this is a question vector, save it
   if ($id !~ /_C\d+$/) {
      @qVect = split /\t/, $vect;
      $qID = $id;
   }
   else {
      my @cVect = split /\t/, $vect;
      my $cosine = &calcCosine(\@qVect, \@cVect);
      print "$qID\t$id\t$cosine\n";
   }

}
close VECTORS or die "Failed to close $VECTORS_FILE_NAME";


################
###   SUBS   ###
################

sub calcCosine() {
   my ($vect1, $vect2) = @_;
   my ($sum11, $sum12, $sum22)= (0.0, 0.0, 0.0);
   for (my $ind = 0; $ind <= $#{$vect1}; $ind++) {
      $sum11 += $$vect1[$ind] * $$vect1[$ind];
      $sum12 += $$vect1[$ind] * $$vect2[$ind];
      $sum22 += $$vect2[$ind] * $$vect2[$ind];
   }
   return 0.0 if ((0 == $sum11) || (0 == $sum22));
   my $cosine = $sum12 / sqrt ($sum11 * $sum22);
   return $cosine;
}
