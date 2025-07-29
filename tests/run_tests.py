import subprocess
import sys

if __name__ == "__main__":
    command = [
        sys.executable,
        "-m",
        "pytest",
        # "-m not requires_license",  # deselect tests that require license to run
    ]

    # Run the command using subprocess.run
    # capture_output=False will print stdout/stderr directly to the console
    # check=True will raise an exception if the command returns a non-zero exit code (i.e., tests failed)
    result = subprocess.run(command, capture_output=False, text=True, check=False)