#!bin/bash
read cnt
for ((i = 1; i <= cnt; i++)); do
	out_file="Testcases/tc${i}.txt"
	python3 game.py > ${out_file}
	echo $i
done