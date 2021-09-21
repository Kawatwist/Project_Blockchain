case $1 in "1")  echo "Master"; python3 -B Main.py --node Full --port 4242 --host localhost --portNode 4243 --portClient 4343 --new True --name Master;;
"2") echo "[1] Connection to Master"; python3 -B Main.py --node Full --port 4243 --host localhost --portNode 4244 --portClient 4344 --name Client1 ;;
"3") echo "[2] Connection to [1]"; python3 -B Main.py --node Full --port 4244 --host localhost --portNode 4245 --portClient 4345 --name Client2 ;;
"4") echo "[3] Connection to Master"; python3 -B Main.py --node Full --port 4243 --host localhost --portNode 4246 --portClient 4346 --name Client3 ;;
"5") echo "[4] Connection to [2]"; python3 -B Main.py --node Full --port 4245 --host localhost --portNode 4247 --portClient 4347 --name Client4 ;;
"6") echo "[5] Connection to [2]"; python3 -B Main.py --node Full --port 4245 --host localhost --portNode 4248 --portClient 4348 --name Client5 ;;
"7") echo "[6] Connection to Master"; python3 -B Main.py --node Full --port 4243 --host localhost --portNode 4249 --portClient 4349 --name Client6 ;;
esac