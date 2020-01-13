#!/usr/bin/perl
#
#  Author: Preslav Nakov
#  
#  Description: Builds thread comments vectors.
#
#  Last modified: July 12, 2016
#
#

use warnings;
use strict;
use utf8;

################
###   MAIN   ###
################

my %threadCommentsVectors = ();

die "One argument expected:" if (0 != $#ARGV);
my $VECTORS_FILE_NAME = $ARGV[0];

### 1. Fetch the vectors file
open(VECTORS, $VECTORS_FILE_NAME) or die "Failed to open $VECTORS_FILE_NAME";
while (<VECTORS>) {
   
   # 1.1. Make sure this is a comment vector
	next if (!/^(Q\d+_R\d+)_C\d+\t([^\n\r]+)[\n\r]*$/);

   # 1.2. Calculate the vector
	my ($id, $vectorText) = ($1, $2);
   my @vector = split /\t/, $vectorText;

   # 1.3. Add the vector to the sum
   if (!defined($threadCommentsVectors{$id})) {
      $threadCommentsVectors{$id}->{VECTOR} = [ @vector ];
   }
   else {
      for (my $ind = 0; $ind <= $#vector; $ind++) {
         $threadCommentsVectors{$id}->{VECTOR}[$ind] += $vector[$ind];
      }
   }
   $threadCommentsVectors{$id}->{CNT}++;
}
close VECTORS or die "Failed to close $VECTORS_FILE_NAME";

### 2. Output the summed vectors
foreach my $relqID (sort keys %threadCommentsVectors) {
   print "$relqID";
   my @vector = @{$threadCommentsVectors{$relqID}->{VECTOR}};
   my $cnt = $threadCommentsVectors{$relqID}->{CNT};
   for (my $ind = 0; $ind <= $#vector; $ind++) {
      print "\t", (1.0 * $vector[$ind] / $cnt);
   }
   print "\n";
}
