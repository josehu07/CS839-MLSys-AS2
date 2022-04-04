# task1
python3 tasks/task1.py | tee task1_result.log
grep "task1-tag" task1_result.log | grep -v "===" > task1.csv

# task2
python3 tasks/task2.py | tee task2_result.log
grep "task2-tag" task2_result.log | grep -v "===" > task2.csv
python3 plot.py --task=2 --csv=task2.csv --out=task2.png

# task3
python3 tasks/task3.py | tee task3_result.log
grep "task3-tag" task3_result.log | grep -v "===" > task3.csv
python3 plot.py --task=3 --csv=task3.csv --out=task3.png
