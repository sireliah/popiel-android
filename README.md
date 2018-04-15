# Popiel for Android
Conceptual game featuring simple genetic algorithm for enemy behaviour.
Background for the game is the Slavic legend of the Popiel that was consumed by mice.
# How to install?
First install requirements.
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
The game uses Cython modules, so compile them first.
```
cd popiel-android
python3 setup.py install
```
When everything is ready, you can start the game!
```
python3 main.py
```
# Mice behaviour
1. Mice record their way through the level and the best result (how far they have gone on the x axis divided by number of steps).
2. The next generation of mice inherit the result with the best score.
3. Mice with no inherited strategy are introduced randomly to the populaton to enrich the list of strategies.


