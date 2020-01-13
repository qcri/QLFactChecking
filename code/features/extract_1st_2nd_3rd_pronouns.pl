#!/usr/bin/perl
#
#  Author: Preslav Nakov
#
#  Description: Extracts 1st, 2nd, 3rd pronoun counts
#
#  Last modified: July 14, 2016
#
#

use warnings;
use strict;
use utf8;

use constant GOOGLE_NEWS_WORDS => 'Google_News_words.txt';

die "Use: $0 <TAB_FORMAT_FILE_TOKENIZED> <SYNTACTIC_PARSE_FILE> <TAB_FORMAT_FILE_NONTOKENIZED>\n" if (2 != $#ARGV);

my $INPUT_FILE        = $ARGV[0];
my $INPUT_FILE_PARSE  = $ARGV[1];
my $INPUT_FILE_NONTOK = $ARGV[2];


#################
####   MAIN   ###
#################

my %googleWords = ();

### Fetch the Google words
open(GOOGLE, GOOGLE_NEWS_WORDS) or die "Failed: $!\n";
while (<GOOGLE>) {
   s/[\n\r]*$//;
   $googleWords{lc $_}++;
}
close GOOGLE or die;

### Open the input file
open(INPUT, $INPUT_FILE) || die "Failed: $!\n";
open(INPUT_NONTOK, $INPUT_FILE_NONTOK) || die "Failed: $!\n";
open(INPUT_PARSE, $INPUT_FILE_PARSE) || die "Failed: $!\n";
binmode(INPUT, ":utf8");
binmode(INPUT_NONTOK, ":utf8");
binmode(INPUT_PARSE, ":utf8");

### Generate the features
my ($qid, $qtext, $qparse, $qtextNontok) = ('', '', '', '');
for (my $lineNo = 1; <INPUT>; $lineNo++) {
   s/[\n\r]+$//;

   # Q268_R16 NA Best Bank. Hi ti all QL's; What bank you are using? and why? Are you using this bank just because it has an affiliate at home? Regards;
   # Q268_R16_C1 Bad   banks are using us ... Talk to those who had taken a credit card or loan to know more ...
   # Check if this is a question
   if (/^(Q[0-9_R]+)\tNA\t(.+)$/) {
      ($qid, $qtext) = ($1, $2);
      $qparse = <INPUT_PARSE>;
      $qtextNontok = <INPUT_NONTOK>;
   }
   # It should be a comment otherwise
   elsif (/^(Q[0-9_R]+_C[0-9]+)\t(True|False)\t(.+)$/) {
      my ($cid, $ctext) = ($1, $3);
      die "Wrong file format!" if ($cid !~ /^$qid\_C[0-9]+$/);

      my $cparse = <INPUT_PARSE>;
      my $ctextNontok = <INPUT_NONTOK>;

      print "$cid";

      ## 34. Extract the personal pronouns
      print "\t", &findPronounCounts($cparse);

      print "\n";
   }
   else {
      die "Wrong file format: '$_'";
   }
}

### Close the files
close INPUT or die;
close INPUT_PARSE or die;
close INPUT_NONTOK or die;


################
###   SUBS   ###
################

sub countOccurences() {
   my ($text, $str) = @_;
   my @arr = split /$str/, $text;
   return $#arr;
}

sub findPronounCounts() {
    my $parse = shift;

    my @firstPronouns = ('i', 'we', 'me', 'us', 'my', 'our', 'mine', 'ours');
    my @secondPronouns = ('you', 'your', 'yours');
    my @thirdPronouns = ('he', 'they', 'him', 'them', 'his', 'her', 'their', 'she', 'her', 'hers', 'theirs', 'it', 'its');

    my $fp_count = 0;
    my $sp_count = 0;
    my $tp_count = 0;

    my (%first, %second, %third) = ();
    $first{$_}++ for (@firstPronouns);
    $second{$_}++ for (@secondPronouns);
    $third{$_}++ for (@thirdPronouns);

    while ($parse =~ s/\(PRP ([^\)]+)\)//) {
      my $pronoun = lc $1;
      if (defined $first{$pronoun}) {
        $fp_count++;
      }
      elsif (defined $second{$pronoun}) {
        $sp_count++;
      }
      elsif (defined $third{$pronoun}) {
        $tp_count++;
      }
    }
    my $totalPronCnt = $fp_count + $sp_count + $tp_count;
    return ("$fp_count\t$sp_count\t$tp_count" 
      . "\t" . (1.0 * $fp_count / ($totalPronCnt > 0 ? $totalPronCnt : 1))
      . "\t" . (1.0 * $sp_count / ($totalPronCnt > 0 ? $totalPronCnt : 1))
      . "\t" . (1.0 * $tp_count / ($totalPronCnt > 0 ? $totalPronCnt : 1))
      . "\t$totalPronCnt");
}

sub getTokensCount() {
   my $text = shift;
   my @arr = split /[ \t]+/, $text;
   return (1 + $#arr);
}

sub getType2TokenRatio() {
   my $text = shift;
   my %tokens = ();
   my @arr = split /[ \t]+/, $text;
   foreach my $token (@arr) {
      $tokens{$token}++;
   }
   return (keys %tokens) / (1.0 + $#arr);
}

sub getSentenceCount() {
   my $parse = shift;
   my @arr = split /\(\./, $parse;
   return (1 + $#arr);
}

sub getPOSCount() {
   my ($parse, $posTagPrefix) = @_;
   my @arr = split /\($posTagPrefix/, $parse;
   return $#arr;
}

sub getNumberWordsNotInGoogle() {
   my $text = shift;
   my $cnt = 0;
   foreach my $token (split /[ \t]+/, lc $text) {
      next if ($token !~ /[a-z]/);
      if (!defined($googleWords{$token})) {
         $cnt++;
      }
   }
   return $cnt;
}
