from cx_Freeze import setup, Executable

base = None

executables = [Executable("App.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
    name = "Naive Bayes Classifier",
    options = options,
    version = "1.0",
    description = 'Programa que permite clasificar nuevas tuplas con base en probabilidades de un conjunto',
    executables = executables
)
