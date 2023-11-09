#!/usr/bin/perl

use strict;

use File::Type;
use File::stat qw(:FIELDS);
use CGI qw/:standard/;

my $base = "/sites/r.sine.com";
my @pictures;
my $period = time() - 604800 ; # new equals the last two weeks

my @seenPics = cookie('seen'); my $seen;
my $q=new CGI;

opendir DIR, "$base"; my $file;

while ( defined ($file = readdir DIR) ) { unless ($file =~ /^\./) {

 	my $show++ if ($file =~ /\.(jpg|jpeg|gif|png)$/);
	my $step;
	while ( !$seen and ($step <= scalar(@seenPics)) ) {
		$seen++ if $file eq $seenPics[$step];
		$step++;
	}
	undef $step;

	if ($q->param('new')) {
 		my $st = stat("$base/$file");
		push @pictures, $file
		if ( $st_ctime ge $period and $show and !$seen ) ;

	} else {
		push @pictures, $file if $show and !$seen ; }

	undef $show; undef $seen;
 	undef $file;

} } closedir DIR;


srand();
my $this = $pictures[int(rand(scalar(@pictures)))];
push @seenPics, $this if !$seen;

open HISTORY, ">> $base/HISTORY";
print HISTORY "$ENV{REMOTE_ADDR}\t$this\n";
close HISTORY;

my $ft = File::Type->new();
my $type = $ft->mime_type("$base/$this");

my $c = cookie(-name    =>  'seen',
            -value   =>  \@seenPics,
            -domain  =>  'r.sine.com',
            );
print "Set-Cookie: ",$c->as_string,"\n";

if ($q->param('html')) {
	print header();
	print "<body><img src=\"$this\"></body><p>http://r.sine.com/$this</p>";
} else {

	print header(-type => "$type");
	open FILE, "$base/$this";
	foreach (<FILE>) { print $_; }
	close FILE;
}