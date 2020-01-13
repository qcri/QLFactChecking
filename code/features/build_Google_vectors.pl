#!/usr/bin/perl
#
#  Author: Preslav Nakov
#  
#  Description: Builds Google vectors
#
#  Last modified: January 22, 2016
#
#

use warnings;
use strict;
use utf8;

use constant OUTPUT_VECTORS_DIFF   => 0;
use constant FILTER_PUNC           => 1;

use constant VECTOR_DIMENSIONALITY => 300;
my $INPUT_FILE  = $ARGV[0];

my $OUTPUT_FILE = $INPUT_FILE . '.word2vec.300d.vectors.all_tokens';
use constant VECTORS_FILE => '/Users/preslav/Dropbox (QCRI)/QCRI/ALT-MT/Discourse for MT/NAACL2015/data/word2vec_GoogleNews/GoogleNews-vectors-negative300.bin.txt.gz';



#################
####   MAIN   ###
#################

my %wordsNeeded = ();
my %word2ScoresArr = ();


### I. Build a list of words
print "Building dictionary...\n";
&buildDictionary($INPUT_FILE, \%wordsNeeded);

### II. Fetch the vectors
print "Reading word vectors...\n";
&fetchVectorsFile(VECTORS_FILE, \%word2ScoresArr, \%wordsNeeded);

### III. Generating the vectors
print "Generating vectors...\n";
open INPUT, $INPUT_FILE or die;
binmode(INPUT, ":utf8");
open OUTPUT, '>' . $OUTPUT_FILE or die;

while (<INPUT>) {
   my $text = $_;

   my @vector = &getVector($text);

   ### Output the vector
   for (my $ind = 0; $ind < VECTOR_DIMENSIONALITY; $ind++) {
      print OUTPUT "\t" if ($ind > 0);
      print OUTPUT ($vector[$ind]);
   }

   ### Add a new line at the end
   print OUTPUT "\n";

}
close INPUT  or die;
close OUTPUT or die;

print "done.\n";


################
###   SUBS   ###
################

sub fetchVectorsFile() {
   my ($fname, $vectors, $words2get) = @_;
   open INPUT, 'gunzip -c "'. $fname . '" | ' or die;
   while (<INPUT>) {
      # the 0.418 0.24968 -0.41242 0.1217 0.34527 -0.044457 -0.49688 -0.17862 -0.00066023 -0.6566 0.27843 -0.14767 -0.55677 0.14658 -0.0095095 0.011658 0.10204 -0.12792 -0.8443 -0.12181 -0.016801 -0.33279 -0.1552 -0.23131 -0.19181 -1.8823 -0.76746 0.099051 -0.42125 -0.19526 4.0071 -0.18594 -0.52287 -0.31681 0.00059213 0.0074449 0.17778 -0.15897 0.012041 -0.054223 -0.29871 -0.15749 -0.34758 -0.045637 -0.44251 0.18785 0.0027849 -0.18411 -0.11514 -0.78581 
      die "Wrong file format: $_" if (!/^([^ \t]+)[ \t]([0-9\-\.e \t]+)[\n\r*]$/);
      my ($word, $scores) = (lc $1, $2);
      next if (!defined($$words2get{$word}));
      next if (FILTER_PUNC && ($word !~ /[a-zA-Z0-9]/));
      my @scoresArr = split /[ \t]+/, $scores;
      die "Wrong dimensionality: $#scoresArr" if ($#scoresArr + 1 != VECTOR_DIMENSIONALITY);
      $$vectors{$word} = \@scoresArr;
   }
   close INPUT or die;
}


sub buildDictionary() {
   my ($inputFile, $words) = @_;
   open INPUT, $inputFile or die;
   binmode(INPUT, ":utf8");
   while (<INPUT>) {
      my $text = $_;

      ### Calculate lowercased vector sum
      foreach my $word (split /[ \t]+/, lc $text) {
          $$words{$word}++;
      }
   }
   close INPUT or die;
}


sub getVector() {
   my $text = shift;
  
   ### Calculate vector sum
   my @vectorSum = (0) x VECTOR_DIMENSIONALITY;
   my $knownWordsCnt = 0;
   foreach my $word (split /[ \t]+/, lc $text) {
      next if (!defined($word2ScoresArr{$word}));
      $knownWordsCnt++;
      my @vect = @{$word2ScoresArr{$word}};
      for (my $ind = 0; $ind < VECTOR_DIMENSIONALITY; $ind++) {
         $vectorSum[$ind] += $vect[$ind];
      }
   }

   ### Normalize the vector
   if ($knownWordsCnt > 0) {
      for (my $ind = 0; $ind < VECTOR_DIMENSIONALITY; $ind++) {
         $vectorSum[$ind] /= $knownWordsCnt;
      }
   }

   ### Return the result
   return @vectorSum;
}


sub calcCosine() {
   my ($vect1, $vect2) = @_;
   my ($sum11, $sum12, $sum22)= (0.0, 0.0, 0.0);
   for (my $ind = 0; $ind < VECTOR_DIMENSIONALITY; $ind++) {
      $sum11 += $$vect1[$ind] * $$vect1[$ind];
      $sum12 += $$vect1[$ind] * $$vect2[$ind];
      $sum22 += $$vect2[$ind] * $$vect2[$ind];
   }
   return 0.0 if ((0 == $sum11) || (0 == $sum22));
   my $cosine = $sum12 / sqrt ($sum11) / sqrt($sum22);
   return $cosine;
}
