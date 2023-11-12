#### How to Install

First, make sure that you have [python](https://www.python.org/downloads/) in your computer.

1.Clone [**this repository**](https://github.com/thanidacwn/veggie-hub) by type this command in your terminal at your choosen path:

```sh
git clone https://github.com/thanidacwn/veggie-hub veggie-hub
```
go to project directory

```sh
cd veggie-hub
```

2.Create a virtual env directory named "env"
```sh
python3 -m venv  env
```

Then, also make sure you have [Node.js](https://nodejs.org/en/download/current) in your computer.

1.Change NPM_BIN_PATH in your env file according to your Node.js' npm path in your computer.
```dotenv
# example:
NPM_BIN_PATH="C:\Program Files\node.js\npm.cmd"
```

2.Finally, you should be able to use Tailwind CSS classes in HTML. Start it by running the following command:
```sh
python3 manage.py tailwind start
```