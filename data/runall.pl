#!/usr/bin/perl

use strict;
use threads;
use Thread qw(async);
use Thread::Queue;
use Thread::Semaphore;

use Getopt::Long;
Getopt::Long::config('bundling_override');
   
my %options;
GetOptions(\%options,'n=s');

my $nT=$options{'n'} ? $options{'n'} : 2;

my $semaphore=new Thread::Semaphore;

my $cmsDriver_commands="cmsDriver_commands.txt";
open(DAT, $cmsDriver_commands) || die("Could not open file!");
my @cfgs=<DAT>;

my $counter : shared = 0;

my @thrs;
for ( my $i=0; $i<$nT; $i++) {
    $thrs[$i]= new Thread \&thread_sub, $i;
}

for ( my $i=0; $i<$nT; $i++) {
    my @d1=($thrs[$i])->join;
}

sub thread_sub {
    my $subnum=shift @_;
    my $done=0;
    while ( $done == 0 ) {
	$semaphore->down;
	my $c=$counter;
	$counter++;
	$done=1 if ( $c > $#cfgs );
	$semaphore->up;

	my @sp2=split('\n',$cfgs[$c]);
	my $cfg=$sp2[0];

	if ( $done == 0 ) {
	    my @thesplittedline=split(' ',$cfgs[$c]);
            my $logF=@thesplittedline[1];
	    $logF.=".log";
	    if ( -e $logF) {
		my $old=$logF;
		$old.=".old";
		unlink $old;
		rename $logF,$old;
	    }
            print "Executing: $cfg\n";
	    system("eval `scramv1 run -sh`; $cfg 1> $logF 2> $logF");
	    open F1, $logF;
	    my $status=0;
	    while (<F1> ) {
		if ( $_ =~ /TrigReport Events total/ ) {
		    $status=1;
		    my @sp=split(' ',$_);
		    my $nP=$sp[7];
		    $status=2 if ( $nP==0);
		}
	    }
	    close F1;
	    print "Done with $cfg : ";
	    print "PASSED\n"  if ( $status==1);
	    print "ABORTED?? (no end of job printouts)\n" if ( $status==0);
	    print "FAILED\n" if ( $status==2);
	}
    }

}
