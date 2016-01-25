raspivid -t 999999 -o - | nc -l -p 5001 &
