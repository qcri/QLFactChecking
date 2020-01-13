#!/usr/bin/perl
#
#  Author: Preslav Nakov
#  
#  Description: Extracts data from ql_user_features_all_forum_stats
#
#  Last modified: July 13, 2016
#
#

use warnings;
use strict;
use utf8;

use open qw(:std :utf8);

use constant MAX_COMMENT_OR_QUESTION_LENGTH => 1000;
use constant STATS_FILE_NAME => 'ql_user_features_all_forum_stats.tsv';


################
###   MAIN   ###
################

my %user2Feats = ();
my $sampleFeats = '';

### 1. Fetch the statistics
open STATS, 'cut -f1,6-23,25 "'. STATS_FILE_NAME . '" | ' or die;
binmode(STATS, ":utf8");
$_ = <STATS>; ## Skip the first line
while (<STATS>) {
	next if (/^\"20/);
	die "Wrong file format: '$_'" if (!/^([^\t]*)\t([\d\t\.]+)[\n\r]*$/);
	my ($userName, $features) = ($1, $2);
	$userName =~ s/\"//g;
	if (length $userName > 0) {
		$user2Feats{$userName} = $features;
		$sampleFeats = $features;
	}
}
close STATS or die;


### 2. Process the XML file and output the corresponding features
$sampleFeats =~ s/[\d\.]+/0/g;
while (<>) {

	# # <RelQuestion RELQ_ID="Q100195_R1" RELQ_CATEGORY="Visas and Permits" RELQ_DATE="2008-06-05 15:00:20" RELQ_USERID="U156" RELQ_USERNAME="smithbits" RELQ_ID_ORIG="20400246" RELQ_USERID_ORIG="3273081">
	# if (/<RelQuestion RELQ_ID=\"(Q\d+_R\d+)\".+RELQ_USERNAME=\"([^\"]+)\"/) {
	# 	my ($qID, $qUserName) = ($1, $2);
	# 	if (defined $user2Feats{$qUserName}) {
	# 		print "$qID\t$user2Feats{$qUserName}\n";
	# 	}
	# 	else {
	# 		print STDERR "Undefined: '$qUserName'\n";
	# 	}
	# }

	# <RelComment RELC_ID="Q100195_R1_C1" RELC_DATE="2008-06-05 15:13:36" RELC_USERID="U2" RELC_USERNAME="anonymous" RELC_ID_ORIG="4680007" RELC_USERID_ORIG="2019916" RELC_RELEVANCE2RELQ="Good" RELC_CREDIBLE="Credible">
	if (/<RelComment .+ RELC_ID=\"(Q\d+_R\d+_C\d+)\".+RELC_USERNAME=\"([^\"]+)\"/) {
		my ($cID, $cUserName) = ($1, $2);
		if (defined $user2Feats{$cUserName}) {
			print "$cID\t$user2Feats{$cUserName}\n";
		}
		else {
			print STDERR "Undefined($cID): '$cUserName'\n";
			print "$cID\t$sampleFeats\n";
		}
	}

}
