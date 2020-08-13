# INSTALL
1. Create environment venv inside `tmp` folder: create tmp folder `mkdir tmp`
    - Run `python3 -m venv tmp/venv`
    - Or `Ctrl + Alt + s` (in Pycharm)
        - Select tab: `Project: commerce`
        - Select: `Python3 Interpreter`
        - Add new environment, choose path `/commerce/tmp/venv`

2. Select environment venv: `source tmp/venv/bin/active`
3. Run install packages: `pip3 install -r requirements.txt`
4. Run migrate: `python3 manage.py migrate`
5. Run project: `python3 manage.py runserver`
------------------
