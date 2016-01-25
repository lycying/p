tmp=$(mktemp /tmp/XXX.jpg)
webp=$(basename $tmp .jpg).webp
raspistill -vf -o $tmp
cwebp $tmp -o /dev/stdout
rm -f $tmp
