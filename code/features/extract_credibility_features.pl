#!/usr/bin/perl
#
#  Author: Preslav Nakov
#  
#  Description: Extracts some credibility features.
#
#  Last modified: July 15, 2016
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
my $OUTPUT_FILE       = $ARGV[0] . '.credibility';


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
open(OUTPUT, '>' . $OUTPUT_FILE) || die "Failed: $!\n";
binmode(INPUT, ":utf8");
binmode(INPUT_NONTOK, ":utf8");
binmode(INPUT_PARSE, ":utf8");
binmode(OUTPUT, ":utf8");

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
   elsif (/^(Q[0-9_R]+_C[0-9]+)\t(Credible|NonCredible)\t(.+)$/) {
      my ($cid, $ctext) = ($1, $3);
      die "Wrong file format!" if ($cid !~ /^$qid\_C[0-9]+$/);

      my $cparse = <INPUT_PARSE>;
      my $ctextNontok = <INPUT_NONTOK>;

      print OUTPUT "$cid";

      ## 1. Extract the number of URLs
      print OUTPUT "\t", &countOccurences($ctext, '@URL');

      ## 2. Extract the number of emails
      print OUTPUT "\t", &countOccurences($ctext, '@EMAIL');

      ## 3. Extract the number of phone numbers
      print OUTPUT "\t", &countOccurences($ctext, '@TEL');

      ## 4. Extract the number of images
      print OUTPUT "\t", &countOccurences($ctext, '@IMG');

      ## 6. Extract the comment length in tokens
      my $commentLength = &getTokensCount($ctext); 
      print OUTPUT "\t", $commentLength;

      ## 7. Extract the comment length in sentences
      my $csentCnt = &getSentenceCount($cparse);
      print OUTPUT "\t", $csentCnt;

      ## 8. Calculate the average sentence length in the comment
      print OUTPUT "\t", (1.0 * $commentLength / $csentCnt);

      ## 9. Extract the comment type to token ratio
      print OUTPUT "\t", &getType2TokenRatio($ctext);

      ## 10. Extract the number of nouns in the comment: NN*
      my $cnounCnt = &getPOSCount($cparse, 'NN');
      print OUTPUT "\t", $cnounCnt;

      ## 11. Extract the number of verbs in the comment: VB*
      my $cverbCnt = &getPOSCount($cparse, 'VB');
      print OUTPUT "\t", $cverbCnt;

      ## 12. Extract the number of adjectives in the comment: JJ*
      my $cadjCnt = &getPOSCount($cparse, 'JJ');
      print OUTPUT "\t", $cadjCnt;

      ## 13. Extract the number of adverbs in the comment: RB*
      my $cadvCnt = &getPOSCount($cparse, 'RB');
      print OUTPUT "\t", $cadvCnt;

      ## 14. Extract the number of pronouns in the comment: PRP*
      my $cpronounCnt = &getPOSCount($cparse, 'PRP');
      print OUTPUT "\t", $cpronounCnt;

      ## 15. Calculate the number of question sentences in a comment
      my $cQuestionSentencesCnt = &countOccurences($cparse, '\(\. \?\)');
      print OUTPUT "\t", $cQuestionSentencesCnt;


      ## 23. Extract the number of smileys: ";", ":)" or ":p"
      my $smileysCnt = &countOccurences(lc $ctextNontok, ':p') + &countOccurences($ctextNontok, ':\)') + &countOccurences($ctextNontok, ';\)');
      print OUTPUT "\t", $smileysCnt;

      ## 24. Count the exlamation marks in the comment
      print OUTPUT "\t", &countOccurences($ctextNontok, '!');

      ## 25. Count the double exlamation marks in the comment
      print OUTPUT "\t", &countOccurences($ctextNontok, '\!\!');

      ## 26. Count the triple exlamation marks in the comment
      print OUTPUT "\t", &countOccurences($ctextNontok, '\!\!\!');

      ## 27. Count the question marks in the comment
      print OUTPUT "\t", &countOccurences($ctextNontok, '\?');

      ## 28. Count the double question marks in the comment
      print OUTPUT "\t", &countOccurences($ctextNontok, '\?\?');

      ## 29. Count the triple question marks in the comment
      print OUTPUT "\t", &countOccurences($ctextNontok, '\?\?\?');

      ## 30. Count the number of words that are not in Google News
      my $ctextNonGoogleTokens = &getNumberWordsNotInGoogle($ctext);
      print OUTPUT "\t", $ctextNonGoogleTokens;

      ## 31. Calculate the proportion of comment words that are not in Google News
      print OUTPUT "\t", ($ctextNonGoogleTokens + 1.0) / ($commentLength + 1.0); # smooting to avoid division by zero

      ## 33. Extract the number of inverse smileys: ":(" and ";("
      my $smileysInvCnt = &countOccurences($ctextNontok, ':\(') + &countOccurences($ctextNontok, ';\(');
      print OUTPUT "\t", $smileysInvCnt;


      ## 34. Extract the personal pronouns
      print OUTPUT "\t", &findPronounCounts($cparse);


      print OUTPUT "\n";
   }
   else {
      die "Wrong file format: '$_'";
   }
}

### Close the files
close INPUT or die;
close INPUT_PARSE or die;
close INPUT_NONTOK or die;
close OUTPUT or die;


################
###   SUBS   ###
################

sub countOccurences() {
   my ($text, $str) = @_;
   my @arr = split /$str/, $text;
   return $#arr;
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
