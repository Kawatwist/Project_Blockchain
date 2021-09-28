case $1 in "1")  echo "Master"; python3 -B Main.py --nodeType Genesis --host "localhost" --nodePort 4243 --clientPort 4343 --master True --name Genesis;;
"2") echo "[1] Connection to Master"; python3 -B Main.py --nodeType Full --hostPort 4243 --host "localhost" --nodePort 4244 --clientPort 4344 --name Client1 ;;
"3") echo "[2] Connection to [1]"; python3 -B Main.py --nodeType Full --hostPort 4244 --host "localhost" --nodePort 4245 --clientPort 4345 --name Client2 ;;
"4") echo "[3] Connection to Master"; python3 -B Main.py --nodeType Full --hostPort 4243 --host "localhost" --nodePort 4246 --clientPort 4346 --name Client3 ;;
"5") echo "[4] Connection to [2]"; python3 -B Main.py --nodeType Full --hostPort 4245 --host "localhost" --nodePort 4247 --clientPort 4347 --name Client4 ;;
"6") echo "[5] Connection to [2]"; python3 -B Main.py --nodeType Full --hostPort 4245 --host "localhost" --nodePort 4248 --clientPort 4348 --name Client5 ;;
"7") echo "[6] Connection to Master"; python3 -B Main.py --nodeType Full --hostPort 4243 --host "localhost" --nodePort 4249 --clientPort 4349 --name Client6 ;;
esac