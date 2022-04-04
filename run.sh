# task1
python3 tasks/task1.py | tee task1_result.log
grep task1 task1_result.log > task1.csv

# task2
python3 tasks/task2.py | tee task2_result.log
grep task2 task2_result.log > task2.csv

# task3
python3 tasks/task3.py | tee task3_result.log
grep task3 task3_result.log > task3.csv
