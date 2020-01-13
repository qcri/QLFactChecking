#!/usr/bin/perl
#
#  Author: Preslav Nakov
#  
#  Description: Extracts features using the unigrams from Saif Mohammed's lexicons.
#
#  Last modified: July 13, 2016
#
#

use warnings;
use strict;
use utf8;

use open qw(:std :utf8);


#################
####   MAIN   ###
#################

die "Two file names expected as parameters" if (1 != $#ARGV);
my $DICT_FILE_NAME  = $ARGV[0];
my $INPUT_FILE_NAME = $ARGV[1];

my %pmiScores = ();

### 1. Fetch the PMI words
open (PMI, 'gunzip -c ' . $DICT_FILE_NAME . ' | ') or die;
binmode(PMI, ":utf8");
while (<PMI>) {

   #   #excellent 7.247 2612  3
   die "Wrong format: '$_'" if (!/^([^\t]+)\t([\d\.\-eE]+)\t\d+\t\d+[\n\r]*$/);
   my ($word, $score) = ($1, $2);

   $word = lc $word;
   $pmiScores{$word} = $score;
}
close PMI or die;

### 2. Calculate the scores
open (INPUT, $INPUT_FILE_NAME) or die;
while (<INPUT>) {

   # Q126201_R63_C2  Credible go to the body shop in Villagio , they have these oils there . 
   if (/^(Q\d+\_R\d+\_C\d+)\t(True|False)\t([^\t]+)[\n\r]*$/) {
      my ($cid, $tokenizedText) = ($1, $3);
      $tokenizedText = lc $tokenizedText;

      my ($cntPos, $cntNeg, $sumPos, $sumNeg, $minNeg, $maxPos) = (0, 0, 0.0, 0.0, 0.0, 0.0);
      foreach my $token (split / +/, $tokenizedText) {
         if (defined $pmiScores{$token}) {
            if ($pmiScores{$token} >= 0) {
               $cntPos++;
               $sumPos += $pmiScores{$token};
               if ($pmiScores{$token} > $maxPos) {
                  $maxPos = $pmiScores{$token};
               }
            }
            else {
               $cntNeg++;
               $sumNeg += $pmiScores{$token}; 
               if ($pmiScores{$token} < $minNeg) {
                  $minNeg = $pmiScores{$token};
               }
            }
         }
      }

      my $totalSum = $sumPos + $sumNeg;
      my ($pctPos, $pctNeg) = (0.0, 0.0);
      if (($cntPos + $cntNeg) > 0) {
         $pctPos = $cntPos * 1.0 / ($cntPos + $cntNeg);
         $pctNeg = $cntNeg * 1.0 / ($cntPos + $cntNeg);
      }
      print "$cid\t$cntPos\t$cntNeg\t$pctPos\t$pctNeg\t$sumPos\t$sumNeg\t$totalSum\t$maxPos\t$minNeg\n";

   }

}
close INPUT or die;
