#!/usr/bin/perl
#
#  Author: Preslav Nakov
#  
#  Description: Extracts trollness features.
#
#  Last modified: July 13, 2016
#
#

use warnings;
use strict;
use utf8;

use open qw(:std :utf8);

use constant STATS_FILE_NAME => 'ql_users_troll.tsv';


################
###   MAIN   ###
################

my %user2Feats = ();
my $sampleFeats = '';

### 1. Fetch the statistics
open STATS, STATS_FILE_NAME or die;
binmode(STATS, ":utf8");
$_ = <STATS>; ## Skip the first line
while (<STATS>) {
	die "Wrong file format: '$_'" if (!/^([^\t]*)\t([\d\t\.]+)[\n\r]*$/);
	my ($userName, $features) = ($1, $2);
	$userName =~ s/\"//g;
	$user2Feats{$userName} = $features;
	$sampleFeats = $features;
}
close STATS or die;


### 2. Process the XML file and output the corresponding features
$sampleFeats =~ s/[\d\.]+/0/g;
while (<>) {

	# <RelComment RELC_DATE="2009-03-17 08:27:07" RELC_FACT_LABEL="True" RELC_ID="Q273_R39_C2" RELC_RELEVANCE2RELQ="Good" RELC_USERID="U1199" RELC_USERNAME="kate_n">
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
