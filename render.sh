#!/bin/bash
output=site/$(realpath -s --relative-to="templates" "$1")
echo $output

if [ ! -d "${output%/*}" ]; then
    echo "Creating ${output%/*}"
    mkdir -p ${output%/*}
fi

if [ -f "$output" ]; then
    echo "Removing pre-existing $output"
    rm $output
fi

echo "<!doctype html>" >> $output
echo "<html lang="en">" >> $output

cat components/head.html >> $output

echo "<body>" >> $output

cat components/header.html components/nav.html $1 components/footer.html >> $output

echo "</body>" >> $output
echo "</html>" >> $output
