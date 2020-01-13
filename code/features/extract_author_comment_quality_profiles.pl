#!/usr/bin/perl
#
#  Author: Preslav Nakov
#  
#  Description: Extracts quality profiles for the authors, i.e., were they giving good answers in the past.
#
#  Last modified: July 13, 2016
#
#

use warnings;
use strict;
use utf8;

use open qw(:std :utf8);

use constant AUTHOR_COMMENT_QUALITY_FILE_NAME => 'author_profiles.txt.gz';

my @featureList = ('COUNT_TOTAL', 'COUNT_POSITIVE', 'COUNT_NEGATIVE', 'PERCENT_POSITIVE', 'PERCENT_NEGATIVE', 'SUM_POSITIVE', 'SUM_NEGATIVE', 'SUM_TOTAL', 'AVERAGE_POSITIVE', 'AVERAGE_NEGATIVE', 'AVERAGE_TOTAL', 'MAX_POSITIVE', 'MAX_NEGATIVE');

#################
####   MAIN   ###
#################

my %author2Features = ();

### 1. Fetch the PMI words
open (PROFILE, 'gunzip -c ' . AUTHOR_COMMENT_QUALITY_FILE_NAME . ' | ') or die;
while (<PROFILE>) {

   # 2000851 U61431  "asafadieh"     PERCENT_POSITIVE        1
   die "Wrong format: '$_'" if (!/^\d+\t(U\d+)\t\"[^\"]+\"\t([A-Z\_]+)\t([\d\.\-eE]+)[\n\r]*$/);
   my ($userID, $featName, $featValue) = ($1, $2, $3);

   $author2Features{$userID}{$featName} = $featValue;
}
close PROFILE or die;

### 2. Process the XML file and output the corresponding features
while (<>) {

   # # <RelQuestion RELQ_ID="Q100195_R1" RELQ_CATEGORY="Visas and Permits" RELQ_DATE="2008-06-05 15:00:20" RELQ_USERID="U156" RELQ_USERNAME="smithbits" RELQ_ID_ORIG="20400246" RELQ_USERID_ORIG="3273081">
   # if (/<RelQuestion RELQ_ID=\"(Q\d+_R\d+)\".+RELQ_USERNAME=\"([^\"]+)\"/) {
   #  my ($qID, $qUserName) = ($1, $2);
   #  if (defined $user2Feats{$qUserName}) {
   #     print "$qID\t$user2Feats{$qUserName}\n";
   #  }
   #  else {
   #     print STDERR "Undefined: '$qUserName'\n";
   #  }
   # }

   # <RelComment RELC_ID="Q100195_R1_C1" RELC_DATE="2008-06-05 15:13:36" RELC_USERID="U2" RELC_USERNAME="anonymous" RELC_ID_ORIG="4680007" RELC_USERID_ORIG="2019916" RELC_RELEVANCE2RELQ="Good" RELC_CREDIBLE="Credible">
   if (/<RelComment .+ RELC_ID=\"(Q\d+_R\d+_C\d+)\".+RELC_USERID=\"(U\d+)\"/) {
      my ($cID, $cUserID) = ($1, $2);
      print "$cID";
      foreach my $featName (@featureList) {
         if (defined $author2Features{$cUserID}) {
            print "\t$author2Features{$cUserID}{$featName}";
         }
         else {
            print "\t0";
         }
      }
      print "\n";
   }

}
