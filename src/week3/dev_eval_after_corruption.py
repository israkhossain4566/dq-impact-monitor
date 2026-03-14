import subprocess
import sys

def run():
    subprocess.check_call([sys.executable, "-m", "src.week2.sarhan_Inject_corruptions_into_production"])
    subprocess.check_call([sys.executable, "-m", "src.week3.dev_eval_prod_clean"])

if __name__ == "__main__":
    run()