#!/usr/bin/perl
#
#  Author: Preslav Nakov
#  
#  Description: Extracts rank features and also same-author feature for the comments
#
#  Last modified: July 14, 2016
#
#

use warnings;
use strict;
use utf8;

use open qw(:std :utf8);


################
###   MAIN   ###
################

my $goodCommentRank = 1;
my $qUserID = ();
while (<>) {

	# <RelQuestion RELQ_CATEGORY="Opportunities" RELQ_DATE="2010-05-21 20:20:40" RELQ_FACT_LABEL="Single Question - Factual" RELQ_ID="Q272_R51" RELQ_USERID="U5206" RELQ_USERNAME="edfeeoc">
	if (/<RelQuestion .+ RELQ_ID=\"Q\d+_R\d+\" RELQ_USERID=\"([^\"]+)\"/) {
		$qUserID = $1;
		$goodCommentRank = 1;
	}

	# <RelComment RELC_ID="Q100195_R1_C1" RELC_DATE="2008-06-05 15:13:36" RELC_USERID="U2" RELC_USERNAME="anonymous" RELC_ID_ORIG="4680007" RELC_USERID_ORIG="2019916" RELC_RELEVANCE2RELQ="Good" RELC_CREDIBLE="Credible">
	elsif (/<RelComment .+ RELC_ID=\"(Q\d+_R\d+_C(\d+))\".+RELC_USERID=\"([^\"]+)\"/) {
		my ($cID, $cRank, $cUserID) = ($1, $2, $3);
		my $rcRank = 1.0 / $cRank;
		my $rGoodRank = 1.0 / $goodCommentRank;
		my $rcRankArithmetic = 1.1 - 0.1 * $cRank;
		my $rGoodRankArithmetic = 1.1 - 0.1 * $goodCommentRank;
		print "$cID\t$rcRank\t$rcRankArithmetic\t$rGoodRank\t$rGoodRankArithmetic\t", ($qUserID eq $cUserID ? 1 : 0), "\n";
		$goodCommentRank++;
	}

}
