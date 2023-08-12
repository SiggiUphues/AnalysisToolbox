import subprocess
from multiprocessing import Pool
import argparse
from itertools import product
from latqcdtools.base.initialize import initialize, finalize

initialize('HRG.log')

BQSC = "2000"


def task(temp, mode):
    if mode == 1:
        subprocess.run(["python3", "main_HRGLCP.py", "--r", str(r),
                       "--hadron_file", filepath, "--models", "QM", "--T", str(temp)])
    elif mode == 2:
        subprocess.run(["python3", "main_HRGMeasure.py", "--hadron_file", filepath,
                       "--LCP_file", "HRG_LCP_T%0.1f_r0.4QM"%temp, "--bqsc", BQSC, "--obs", "chi"])

parser = argparse.ArgumentParser(
    description='Run different modes of the script.')
parser.add_argument('runMode', type=int, choices=[
                    0, 1, 2, 3], help='The run mode of the script.')
args = parser.parse_args()

r = 0.4
filepath = "../latqcdtools/physics/HRGtables/QM_hadron_list_ext_strange_2020.txt"
NTASKS = 4
temps = range(120, 165, 5)


def main():
    if args.runMode == 0:
        subprocess.run(["python3", "main_HRG_simple.py"])
    elif args.runMode == 1:
        # Creating pairs of temperature and mode
        args_for_tasks = product(temps, [1])
        with Pool(NTASKS) as pool:
            pool.starmap(task, args_for_tasks)
    elif args.runMode == 2:
        args_for_tasks = product(temps, [2])
        with Pool(NTASKS) as pool:
            pool.starmap(task, args_for_tasks)

    else:
        print("Invalid runMode")


if __name__ == '__main__':
    main()
finalize()
