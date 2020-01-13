use strict;
use warnings;

my $input = "yash_rank.tsv";
my $input_new = $ARGV[0];

open(my $input_file, "<", $input) or die ("Error: Opening input file\n");
open(my $input_new_file, "<", $input_new) or die ("Error: Opening input_new file\n");

my %users;
my $i;
while(my $line = <$input_file>) {
    if($line =~ /(U[0-9]+)\t(.+)/) {
        if($1 eq "U44865") {
            print "$line\n";
            last;
        }
        $users{$1} = $2;
    }
    $i++;
}
#print "$i users added\n";
#print "$output\n";
while(my $line = <$input_new_file>) {
    # print "$line\n";
    if($line =~ /<.+RELC_ID="([^"]+)".+RELC_USERID="([^"]+)".+/) {
        # print "$1\t$2\n";
        if(exists($users{$2})) {
            my $auth_feat = $users{$2};
            print "$1\t$auth_feat\n";
        }
        else {
            print STDERR "Missing User: $1\t$2\n";
            print "$1\t0\t0\t0\t0\n";
        }

    }
}

close $input_file;
close $input_new_file;
