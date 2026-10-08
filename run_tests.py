import os
import sys
import subprocess
import shutil

# Configure UTF-8 encoding for Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def get_allure_bin(project_dir):
    """Locate the executable path of Allure CLI."""
    # Check in local project tools directory
    local_allure = os.path.join(project_dir, "tools", "allure-2.32.0", "bin", "allure.bat")
    if os.path.exists(local_allure):
        return local_allure
    # Check in system PATH
    system_allure = shutil.which("allure")
    if system_allure:
        return system_allure
    return None


def main():
    print("=" * 70)
    print("   AUTOMATION TEST SUITE - UTC ELECTRONIC OFFICE (E-OFFICE)   ")
    print("   Course: Software Testing | Student: Pham Cong Duc - ID: 6451071021   ")
    print("=" * 70)
    print("Starting automated test execution via PyTest + Selenium + Allure...\n")

    project_dir = os.path.dirname(os.path.abspath(__file__))
    report_file = os.path.join(project_dir, "reports", "report.html")
    allure_results_dir = os.path.join(project_dir, "reports", "allure-results")
    allure_report_dir = os.path.join(project_dir, "reports", "allure-report")

    # Handle direct Allure report open argument
    if "--allure" in sys.argv:
        allure_bin = get_allure_bin(project_dir)
        if allure_bin:
            print("Opening Allure Report in browser...")
            subprocess.call([allure_bin, "open", allure_report_dir])
            return 0
        else:
            print("Allure CLI not found to open report.")
            return 1

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "-v",
        "--html=" + report_file,
        "--self-contained-html",
        "--alluredir=" + allure_results_dir,
    ]

    # Forward any extra CLI arguments (e.g., --headed)
    user_args = [arg for arg in sys.argv[1:] if arg != "--allure"]
    if user_args:
        cmd.extend(user_args)

    exit_code = subprocess.call(cmd, cwd=project_dir)

    # Automatically generate Allure HTML report if Allure CLI is available
    allure_bin = get_allure_bin(project_dir)
    if allure_bin and os.path.exists(allure_results_dir):
        print("\nGenerating Allure HTML Report...")
        subprocess.call([allure_bin, "generate", allure_results_dir, "-o", allure_report_dir, "--clean"])
        print(f"Allure HTML Report generated at: {allure_report_dir}")

    print("\n" + "=" * 70)
    if exit_code == 0:
        print(">>> RESULT: ALL AUTOMATED TESTS PASSED SUCCESSFULLY! <<<")
    else:
        print(f">>> RESULT: TEST RUN FINISHED WITH FAILURES OR WARNINGS (Exit code: {exit_code}) <<<")

    print("=" * 70)
    print(f"1. Standard HTML Report: {report_file}")
    if allure_bin:
        print(f"2. Allure Interactive Report: {allure_report_dir}")
        print("   To view Allure Report in browser, run: python run_tests.py --allure")
    print("=" * 70)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
