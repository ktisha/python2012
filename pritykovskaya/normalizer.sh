sep="\n"
col=1
no_clear=0
unique=1

# NOTE: words in queries need to be separated by a whitespace
# NOTE: encoding = utf8 (query internally converted to cp1251)

export LANG=ru_RU.UTF-8;

# $#array --- the index of the last element in the array
# => ($#array + 1) --- the length of the array

if [ "$unique" -gt "0"  ]
then
 last_step=" awk -v col=$col -v sep=\"$sep\" '
BEGIN {
 FS = OFS = \" sep \";
}
{
    delete unique_words; delete ws;
    s=\"\";
    n = split(\$col, ws, \"+\");
    for (i = 1; i < NF + 1; i++) {
    if (i != 1) { s = s \" sep \"; }
    if (i != col) {
     s = s \$i;
    } else {
     s = s ws[1];
     unique_words[ws[1]]=1;
     for (j=2; j < n + 1; j++) {
       if (!(ws[j] in unique_words)) {
           s= s \"+\" ws[j];
           unique_words[ws[j]]=1;
       }
     }
    } 
    }
    print s;
}'"

else
 last_step="cat";
fi

cat /dev/stdin | awk -v col=$col '
BEGIN {
 FS = OFS = "'$sep'";
}
{
 $col = tolower($col);
 s = $1;
 if (NF > 1) {
  for (i = 2; i < NF + 1; i++) {
   s = s "'$sep'" $i;
  }
 }
 print s;
}
' | perl -e '
use strict;

# use lib "/work/data/share/yu/search_queries/lib";
use lib "/home/pritykovskaya/Desktop/python_project/lib";

use Time::Local;
use Sys::Syslog;
use Sys::Hostname;
use Encode;

use vars qw(%engine_stats $engine);

# use STraff::Parse1;
use STraff::Parse;

# binmode (STDIN, ":utf8"); 
# binmode (STDOUT, ":utf8");
# use utf8;

while (<STDIN>) {
    chomp;
    my @fields = split(/'$sep'/);
    my $query_string = $fields['$col' - 1];
    
    # $query_string = decode_utf8($query_string);
 
 if ( (defined $query_string) && ($query_string ne "")) {
#   my $words_ref = STraff::Parse1::words($query_string);
   
   $query_string =~ s/ё/е/g;

   my $length_decoded = Encode::from_to($query_string, "utf8", "cp1251");
   my $words_ref;
   if ('$no_clear' > 0) {
    $words_ref = STraff::Parse::words($query_string);
   } else {
    $words_ref = STraff::Parse::words(STraff::Parse::clear_query($query_string));
   }
   my $length_decoded = Encode::from_to($query_string, "cp1251", "utf8");
   for (my $tt=0; $tt < @$words_ref; $tt++) {
    Encode::from_to(@{$words_ref}[$tt], "cp1251", "utf8");
   }
   my $w = join("\+", sort(@$words_ref));
     ### remove the separator in the beginning
        if (substr($w, 0, 1) eq "\+") {
             # all but the first character
                  $w = substr($w, 1);
        }
   my $s="";
   for (my $i = 0; $i < $#fields + 1; $i++) {
     if ($i != '$col' - 1) {
       $s=$s."'$sep'".$fields[$i];
     } else {
       $s=$s."'$sep'".$w;
     }
   }
   ### remove the separator in the beginning
   if (substr($s, 0, 1) eq "'$sep'") {
     # all but the first character
     $s = substr($s, 1);
   }
   print $s."\n";
 }
}
' /dev/stdin | eval $last_step
   

