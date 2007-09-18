#!/usr/bin/perl -w
# Password-generating script, v0.03
use strict;
use Getopt::Std;

sub pick_element (@);
sub array_entropy (@);

my @patterns = ();
my $numtogen = 10;
my %opts;

getopts( "hvbt:n:", \%opts );

if ($opts{"h"}) {
  print << "EOF";
Usage: $0 [-hvb] [-t <template>] [-n <number>]
Options:
  -h: Prints this help message and quits.
  -v: Prints version information.
  -t: Sets password template (default: cvcvcvcdd).
  -n: Sets number of passwords to generate (default 10).
  -b: Calculates number of bits in specified pattern; no passwords generated.
  
Password templates use the following characters:
  c     lowercase consonant
  v     lowercase vowel
  l     lowercase letter
  C     mixed-case consonant
  V     mixed-case vowel
  L     mixed-case letter
  d, D  digit
  p, P  punctuation symbol (from !\@\%^\&-_+=?)
  
EOF
  exit();
}
elsif ($opts{v}) {
  print << "EOF";
Password generator script, version 0.03.
EOF
  exit();
}

if ($opts{"t"}) {
	push @patterns, $opts{"t"};
}

if ($opts{"n"}) {
	if (int($opts{"n"}) > 0) {
        $numtogen = $opts{"n"};
    }
}

if (! @patterns) {
	push @patterns, "cvcvcvcdd";
}

my @LC_CONSONANTS = qw( b c d f g h k l m n p r s t v w x z );
my @LC_VOWELS = qw( a e i o u y );

my @MC_CONSONANTS = @LC_CONSONANTS;
push @MC_CONSONANTS, map { uc $_ } @LC_CONSONANTS;

my @MC_VOWELS = @LC_VOWELS;
push @MC_VOWELS, map { uc $_ } @LC_VOWELS;

my @LC_LETTERS = @LC_CONSONANTS;
push @LC_LETTERS, @LC_VOWELS;

my @MC_LETTERS = @LC_LETTERS;
push @MC_LETTERS, map { uc $_ } @LC_LETTERS;

my @DIGITS = 0 .. 9;
my @PUNCT = qw( ! @ % ^ & - _ + = ? );

my %pools = ( 'c' => \@LC_CONSONANTS,
              'C' => \@MC_CONSONANTS,
              'v' => \@LC_VOWELS,
              'V' => \@MC_VOWELS,
              'l' => \@LC_LETTERS,
              'L' => \@MC_LETTERS,
              'd' => \@DIGITS,
              'D' => \@DIGITS,
              'p' => \@PUNCT,
              'P' => \@PUNCT
              );
              
if ($opts{b}) {
   	# just calculate bits in pattern
   	# no longer assumes each character in pool is distinct
   	foreach my $pattern (@patterns) {
   	    my $valuecount = 1;
   	    my $bits = 0;
   	    
   	    while($pattern =~ /(.)/g) {
   	       # print "@{$pools{$1}}\n";
   	       $valuecount *= scalar @{$pools{$1}};
   	       $bits += array_entropy(@{$pools{$1}});
   	    }
   	    
   	    my $vbits = ( log($valuecount) / log(2) );
   	    print "Pattern: $pattern   Bits: $bits\n";
   	}
   	exit();
}

                
foreach my $pattern (@patterns) {
	# print "$pattern\n";
    for( my $i = 0; $i < $numtogen; $i++ ) {
    	my $temp = $pattern;
    	$temp =~ s/(.)/pick_element(@{$pools{$1}})/ge;
    	print "$temp\n";
    }
}

sub pick_element (@) {
    my @array = @_;
    my $index;
    $index = int( scalar @array * rand() );
    return $array[$index];
}

sub array_entropy (@) {
    my @array = @_;
    my %counts = ();
    foreach my $elt (@array) {
        $counts{$elt}++;
    }
    
    # bits computed by entropy formula S = \sum_i -p_i \log_2 p_i
    # which simplifies to S = \log_2 t - \sum_i c_i/t \log_2 c_i
    # in the case that p_i = c_i/t for all i
    
    # start in natural logs
    my $bits = log(@array);
    
    foreach my $key (keys %counts) {
        #print "$key $counts{$key}\n";
        $bits -= $counts{$key} * log($counts{$key}) / @array;
    }   
    
    # convert to base 2 logs
    $bits /= log(2);
    
    return $bits;
}