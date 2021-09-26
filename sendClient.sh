for (( i=0; i<$1; ++i)); do
    python3 -B Client.py -p $4 pay $2 payed $3 price 5.0
done