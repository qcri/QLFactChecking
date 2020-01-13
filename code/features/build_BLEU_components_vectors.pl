#!/usr/bin/perl
#
#  Author: Preslav Nakov
#  
#  Description: Calculates the components of BLUE for a given input.
#
#  Last modified: July 8, 2016
#
#

use warnings;
use strict;
use utf8;

use Time::Piece;

die "Use: $0 <INPUT_FILE>\n" if (0 != $#ARGV);

my $INPUT_FILE   = $ARGV[0];
my $OUTPUT_FILE  = $ARGV[0] . '.BLEU_components';

my $TMP_HYP_FILE = $ARGV[0] . '.hyp.tmp';
my $TMP_REF_FILE = $ARGV[0] . '.ref.tmp';


#################
####   MAIN   ###
#################

### Fetch the input file
open(INPUT, $INPUT_FILE) || die "Failed: $!\n";
open(OUTPUT, '>' . $OUTPUT_FILE) || die "Failed: $!\n";
binmode(INPUT, ":utf8");
binmode(OUTPUT, ":utf8");

my ($qid, $qtext) = ('', '');
for (my $lineNo = 1; <INPUT>; $lineNo++) {
   s/[\n\r]+$//;

   # Q268_R16 NA Best Bank. Hi ti all QL's; What bank you are using? and why? Are you using this bank just because it has an affiliate at home? Regards;
   # Q268_R16_C1 Bad   banks are using us ... Talk to those who had taken a credit card or loan to know more ...
   # Check if this is a question
   if (/^(Q[0-9_R]+)\tNA\t(.+)$/) {
      ($qid, $qtext) = ($1, $2);
   }
   elsif (/^(Q[0-9_R]+_C[0-9]+)\t(True|False)\t(.+)$/) {
      my ($cid, $ctext) = ($1, $3);
      die "Wrong file format!" if ($cid !~ /^$qid\_C[0-9]+$/);

      &saveLineToFile($TMP_HYP_FILE, $ctext);
      &saveLineToFile($TMP_REF_FILE, $qtext);
      my $cmd = "./multi-bleu-component4line.pl -lc \"" . $TMP_REF_FILE . "\" < \"" . $TMP_HYP_FILE . "\"";
      my $output = `$cmd`;
      print OUTPUT "$cid\t$output";

   }
   else {
      die "Wrong file format: '$_'";
   }
}

close INPUT or die;
close OUTPUT or die;


################
###   SUBS   ###
################

sub saveLineToFile() {
   my ($fileName, $line) = @_;
   open OUT, ">$fileName" or die;
   binmode(OUT, ":utf8");
   print OUT $line;
   flush OUT;
   close OUT or die;
}
