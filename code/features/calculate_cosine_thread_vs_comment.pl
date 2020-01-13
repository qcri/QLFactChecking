#!/usr/bin/perl
#
#  Author: Preslav Nakov
#  
#  Description: Calculates the cosine vectors between a comment and a comment-thread.
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

die "Two arguments expected:" if (1 != $#ARGV);
my $VECTORS_FILE_NAME        = $ARGV[0];
my $VECTORS_FILE_THREAD_NAME = $ARGV[1];

my %threadVects = ();

### 0. Fetch the thread vectors
open(VECTORS_THREAD, $VECTORS_FILE_THREAD_NAME) or die "Failed to open $VECTORS_FILE_THREAD_NAME";
while (<VECTORS_THREAD>) {
   die "Wrong file format!" if (!/^(Q\d+[^\t]*)\t([^\n\r]+)[\n\r]*$/);
   my ($id, $threadVect) = ($1, $2);
   $threadVects{$id} = $threadVect;
}
close VECTORS_THREAD or die "Failed to close $VECTORS_FILE_THREAD_NAME";

### 1. Fetch the vectors file
open(VECTORS, $VECTORS_FILE_NAME) or die "Failed to open $VECTORS_FILE_NAME";
while (<VECTORS>) {

   ### 1. Check the file format and get the vector
	die "Wrong file format!" if (!/^(Q\d+[^\t]*)\t([^\n\r]+)[\n\r]*$/);
   my ($id, $vect) = ($1, $2);

   ### 2. Make sure this is a comment vector
   if ($id =~ /^(.+)_C\d+$/) {
      my $qID = $1;

      # 2.1. Get the comment vector
      my @vect = split /\t/, $vect;

      # 2.2. Get the corresponding vector
      die "Missing thread vector: $qID" if (!defined($threadVects{$qID}));
      my @threadVect = split /\t/, $threadVects{$qID};

      # 2.3. Check whether they match
      die "Vector lengths differ: $#threadVect != $#vect" if ($#threadVect != $#vect);

      # 2.4. Calculate the cosine
      my $cosine = &calcCosine(\@vect, \@threadVect);
      print "$id\t$cosine\n";
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
