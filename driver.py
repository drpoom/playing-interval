import subprocess
import time
import os
import re
import argparse

# --- ANSI COLORS ---
C_RESET, C_BOLD = "\033[0m", "\033[1m"
C_BLUE, C_GREEN = "\033[94m", "\033[92m"
C_YELLOW, C_RED = "\033[93m", "\033[91m"
C_CYAN = "\033[96m"

# --- CONFIGURATION ---
BASE_AGENT_CMD = ["openclaw", "agent", "--agent", "main", "--message"]
GOAL_FILE = "goal.md"
SPRINT_DIR = "./sprints"
TRACE_LOG = "agent_trace.log"

# THE SAFETY LIST: If these are missing, the agent is fired.
PROTECTED_FILES = ["goal.md", "driver.py", "story.md", "theme.md"]

def log(message, color=C_RESET, bold=False):
    style = color + (C_BOLD if bold else "")
    print(f"{C_CYAN}[{time.strftime('%H:%M:%S')}]{C_RESET} {style}{message}{C_RESET}")

def safety_check():
    """Verify that the agent hasn't nuked the project root."""
    missing = [f for f in PROTECTED_FILES if not os.path.exists(f)]
    if missing:
        log(f"CRITICAL SAFETY VIOLATION: {missing} are missing!", C_RED, True)
        log("Emergency Shutdown initiated. Check 'git status'.", C_RED)
        sys.exit(1)

def run_agent_cli(prompt, pi, sprint, step_name="STEP"):
    safety_check() # Check before every interaction
    
    with open(GOAL_FILE, "r") as f:
        goal = f.read()

    full_prompt = (
        f"CONTEXT: PI {pi}.{sprint} | Path: {os.getcwd()}\n"
        f"OBJECTIVE: {goal}\n"
        f"IMPORTANT: Do NOT delete files in the root. Build to 'dist/' only.\n\n"
        f"TASK: {prompt}"
    )
    
    log(f"Agent ({step_name}): Working...", C_YELLOW)
    
    try:
        result = subprocess.run(BASE_AGENT_CMD + [full_prompt], capture_output=True, text=True, timeout=600)
        
        with open(TRACE_LOG, "a") as f:
            f.write(f"\n{'='*40}\nSTEP: {step_name} | {time.strftime('%H:%M:%S')}\nOUT: {result.stdout}\n")

        return result.stdout.strip()
    except Exception as e:
        log(f"System Error: {e}", C_RED); return ""

def verify_and_deploy(pi, sprint):
    log(f"Verifying {pi}.{sprint}...", C_BLUE)
    
    if not os.path.exists("package.json"):
        return False, "package.json missing."
    
    # 0. Ensure dependencies are installed
    subprocess.run(["npm", "install"], capture_output=True, text=True)

    # 1. Build into DIST (Safety check: make sure we don't build to .)
    log("Building to /dist...", C_CYAN)
    b = subprocess.run(["npm", "run", "build"], capture_output=True, text=True)
    
    # Check if the build nuked the root during its run
    safety_check()

    if b.returncode != 0: return False, b.stderr
    
    # 2. Git Push (Our actual recovery point)
    try:
        subprocess.run(["git", "add", "."], check=True)
        diff = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if diff.stdout.strip():
            subprocess.run(["git", "commit", "-m", f"Sprint {pi}.{sprint} SUCCESS"], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            log("State backed up to GitHub.", C_GREEN)
        return True, ""
    except Exception as e:
        log(f"Git Fail: {e}", C_RED); return False, str(e)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-sprint", type=int, default=-1)
    args = parser.parse_args()

    if not os.path.exists(SPRINT_DIR): os.makedirs(SPRINT_DIR)
    
    # Initialize Git if not present (The Ultimate Safety Net)
    if not os.path.exists(".git"):
        log("Initializing Git safety net...", C_YELLOW)
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Initial Safety Point"], check=True)

    pi_id, sprint_id = 1, 1 # Resetting for recovery
    run_count = 0

    while True:
        if args.max_sprint != -1 and run_count >= args.max_sprint: break
        log(f"--- SPRINT {pi_id}.{sprint_id} ---", C_BLUE, True)

        # 1. DEV
        resp = run_agent_cli("Add the next feature. Ensure build output goes to dist/.", pi_id, sprint_id, "DEV")
        
        # 2. VERIFY & BACKUP
        success, err = verify_and_deploy(pi_id, sprint_id)
        if not success:
            log("Build Failed. Repairing...", C_RED)
            run_agent_cli(f"FIX BUILD: {err}", pi_id, sprint_id, "REPAIR")
            success, _ = verify_and_deploy(pi_id, sprint_id)

        sprint_id += 1; run_count += 1; time.sleep(5)

if __name__ == "__main__":
    import sys
    main()

