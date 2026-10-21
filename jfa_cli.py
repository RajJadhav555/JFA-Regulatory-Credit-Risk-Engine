import argparse
import subprocess
import sys

PIPELINE = [
    "JFA_portfolio.py",
    "JFA_stress_test.py",
    "JFA_Expected_loss.py",
    "JFA_masterDashboard.py",
    "JFA_narrative.py",
]

def run_audit():
    for script in PIPELINE:
        print(f"Running: {script}")
        result = subprocess.run(["python3",script])
        if result.returncode !=0:
            print(f"[FAILED] Pipeline halted at: {script}")
            sys.exit(1)
    print("\n[SUCCESS] Full audit pipeline completed")

parser = argparse.ArgumentParser(description="JFA Credit Risk CLI")
subparsers = parser.add_subparsers(dest="command")
subparsers.add_parser("audit", help="Run full risk audit pipeline")
args = parser.parse_args()

if args.command == "audit":
    run_audit()
else:
    parser.print_help()
