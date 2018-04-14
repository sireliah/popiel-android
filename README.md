# Popiel for Android
Conceptual game featuring simple genetic algorithm for enemy behaviour

# How to install?

Install requirements.
```
virtualenv -p python3.6 venv
source venv/bin/activate
pip3 install -r requirements.txt
```
One of the requirements is Kivent lib. The best way is to install it from source.
```
git clone https://github.com/kivy/kivent
cd kivent/modules/core
python3 setup.py install
```
The game uses Cython modules, so ompile them first.
```
cd popiel-android
python3 setup.py install
```
When everything is ready, you can start the game!
```
python3 main.py
```

