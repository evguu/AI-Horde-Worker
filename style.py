import argparse
import glob
import os
import subprocess
import sys

# Set the working directory to where this script is located
os.chdir(os.path.dirname(os.path.abspath(__file__)))

src = [
    "worker",
]

ignore_src = [
    "bridgeData_template.py",
    "bridgeData.py",
]

root_folder_src = glob.glob("*.py")

src.extend(root_folder_src)

src = [item for item in src if item not in ignore_src]

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
    "--fix",
    action="store_true",
    required=False,
    help="Fix issues which can be fixed automatically",
)
args = arg_parser.parse_args()

black_args = [
    "black",
    "--line-length=119",
]
flake8_args = [
    "flake8",
]
isort_args = [
    "isort",
]

if args.fix:
    print("fix requested")
else:
    print("fix not requested")

    black_args.extend(("--check", "--diff"))
    isort_args.extend(("--check-only", "--diff"))
lint_processes = [
    black_args,
    isort_args,
    flake8_args,
]

for process_args in lint_processes:
    process_args.extend(src)

    COMMAND = " ".join(process_args)
    print(f"\nRunning {COMMAND}")
    try:
        subprocess.run(COMMAND, shell=True, check=True)
    except subprocess.CalledProcessError:
        sys.exit(1)
