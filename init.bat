echo off
cls

pip install -r requirements.txt
echo [ Requirements installed ]

flask db init
flask db migrate
flask db upgrade
echo [ Database created ]

python .\cmd\gen_model.py
echo [ Model generated ]