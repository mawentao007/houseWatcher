source /home/users/mawentao03/.bashrc
python houseCheck.py > tmp
cat tmp |mail -s "[HOUSE CHECK]" "862905339@qq.com mawentao03@baidu.com"
