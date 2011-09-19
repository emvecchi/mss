#!/usr/bin/perl -w

use Statistics::RankCorrelation;

use warnings;
use strict;

my @x = ();
my @y = ();
my %h = ();
open F, $ARGV[0] or die "cant open testing file";
while (<F>) {
    my $line = $_;
    my ($w1, $w2, $score) = split /\s+/, $line;
    $h{$w1."_".$w2} = $score;
    

}

close F;
#open F, "/Volumes/Working/Works/Bolzano/Thesis/vision/mmss/evaluation/cleaned-wordsim_similarity_goldstandard.txt" or die "Cant open this file";
open F, "./cleaned-wordsim_similarity_goldstandard.txt" or die "Cant open this file";
#open F, "/Volumes/Working/Works/Bolzano/Thesis/vision/mmss/evaluation/rubenstein-goodeneough.txt" or die "Cant open this file";
open OUT, ">out.$ARGV[0]" or die "cant open out.$ARGV[0] for writing";
while (my $line = <F>) {
    chomp($line); 
    my ($w1, $w2, $score) = split /\s+/, $line;
    if (exists $h{$w1."_".$w2}) {
        push @x, $h{$w1."_".$w2};
        push @y, $score;
        print OUT $line, "\t", $h{$w1."_".$w2}, "\n";
    }
}

my $c = Statistics::RankCorrelation->new (\@x, \@y, sorted => 1);
print "Spreaman\t", $c->spearman, "\n";
close F;
close OUT;
