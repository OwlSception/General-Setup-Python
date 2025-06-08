# update_requirements.py

import subprocess

# import python
import R
import rpy2


def update_requirements():
    with open("requirements.txt", "w") as req_file:
        subprocess.run(["pip", "freeze"], stdout=req_file)


if __name__ == "__main__":
    update_requirements()
