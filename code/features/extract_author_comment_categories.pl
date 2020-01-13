#!/usr/bin/perl
#
#  Author: Preslav Nakov
#  
#  Description: Extracts features based on the categories each author has posted comments in:
#               First raw frequencies, 
#               then normalized frequencies (by total number of comments),
#               then number of posts,
#               then number of categories.
#
#  Last modified: July 13, 2016
#
#

use warnings;
use strict;
use utf8;

use open qw(:std :utf8);

use constant STATS_FILE_NAME => 'author_categories.tsv.gz';


################
###   MAIN   ###
################

my %user2Feats = ();
my %categories = ();

### 1. Fetch the statistics
open STATS, 'gunzip -c "'. STATS_FILE_NAME . '" | ' or die;
binmode(STATS, ":utf8");
while (<STATS>) {
	
	# U44713  Proud Paki      Family Life in Qatar    1
	die "Wrong file format: '$_'" if (!/^(U\d+)\t[^\t]+\t([^\t]+)\t(\d+)[\n\r]*$/);
	my ($userID, $categName, $categFreq) = ($1, $2, $3);

	die "Duplicate for ($userID, $categName)" if (defined $user2Feats{$userID}{$categName});
	$user2Feats{$userID}{$categName} = $categFreq;
	$categories{$categName}++;
}
close STATS or die;


### 2. Process the XML file and output the corresponding features
while (<>) {

	# <RelComment RELC_ID="Q100195_R1_C1" RELC_DATE="2008-06-05 15:13:36" RELC_USERID="U2" RELC_USERNAME="anonymous" RELC_ID_ORIG="4680007" RELC_USERID_ORIG="2019916" RELC_RELEVANCE2RELQ="Good" RELC_CREDIBLE="Credible">
	if (/<RelComment .+ RELC_ID=\"(Q\d+_R\d+_C\d+)\".+RELC_USERID=\"(U\d+)\"/) {
		
		my ($cID, $cUserID) = ($1, $2);
		print "$cID";
		
		# 2.1. Output the raw frequencies first
		my ($totalPosts, $totalCategs) = (0, 0);
		foreach my $categ (sort keys %categories) {
			if (defined $user2Feats{$cUserID}{$categ}) {
				print "\t$user2Feats{$cUserID}{$categ}";
				$totalPosts += $user2Feats{$cUserID}{$categ};
				$totalCategs++;
			}
			else {
				print "\t0";
			}
		}

		# 2.2. Output the normalized frequencies
		foreach my $categ (sort keys %categories) {
			if (defined $user2Feats{$cUserID}{$categ}) {
				my $score = $user2Feats{$cUserID}{$categ} * 1.0 / $totalPosts;
				print "\t$score";
			}
			else {
				print "\t0";
			}
		}

		# 2.3. Output the totals
		print "\t$totalPosts\t$totalCategs\n";

	}

}
