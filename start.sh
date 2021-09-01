source /home/users/m/.bashrc
python houseCheck.py > tmp
cat tmp |mail -s "[HOUSE CHECK]" ""
