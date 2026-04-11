import subprocess
import time
import os
import re
import argparse
import sys

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
PROTECTED_FILES = ["goal.md", "driver.py", "story.md", "theme.md", "sprints"]

def log(message, color=C_RESET, bold=False):
    style = color + (C_BOLD if bold else "")
    print(f"{C_CYAN}[{time.strftime('%H:%M:%S')}]{C_RESET} {style}{message}{C_RESET}")

def get_dir_map():
    """Provides Hans with a map of the current architecture so he can iterate."""
    try:
        # Exclude node_modules and hidden folders to keep the prompt clean
        res = subprocess.run(
            ["find", ".", "-maxdepth", "3", "-not", "-path", "*/.*", "-not", "-path", "./node_modules*"],
            capture_output=True, text=True
        )
        return res.stdout
    except: return "Unable to map directory."

def safety_check():
    """Verify that the agent hasn't nuked the project root."""
    missing = [f for f in PROTECTED_FILES if not os.path.exists(f)]
    if missing:
        log(f"CRITICAL SAFETY VIOLATION: {missing} are missing!", C_RED, True)
        log("Emergency Shutdown initiated. Run 'git reset --hard' to recover.", C_RED)
        sys.exit(1)

def run_agent_cli(prompt, pi, sprint, step_name="STEP"):
    safety_check()
    
    with open(GOAL_FILE, "r") as f:
        goal = f.read()

    # ITERATIVE ARCHITECTURE: We feed the directory map back to the AI
    dir_map = get_dir_map()

    full_prompt = (
        f"OBJECTIVE: {goal}\n"
        f"STATE: PI {pi}.{sprint} | Path: {os.getcwd()}\n"
        f"EXISTING FILES:\n{dir_map}\n"
        f"INSTRUCTION: {prompt}\n"
        f"RULES: \n"
        f"1. Build output to 'dist/'. \n"
        f"2. DO NOT delete existing files unless replacing with improved versions.\n"
        f"3. Use existing components/logic where possible."
    )

    log(f"Agent ({step_name}): Working on {pi}.{sprint}...", C_YELLOW)

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

    log("Building to /dist...", C_CYAN)
    b = subprocess.run(["npm", "run", "build"], capture_output=True, text=True)
    
    safety_check() # Check if root survived the build

    if b.returncode != 0: return False, b.stderr

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

    # --- PROGRESSIVE SPRINT DETECTION ---
    # Scans the sprints folder to see where we left off
    files = os.listdir(SPRINT_DIR)
    pattern = re.compile(r"sprint_(\d+)\.(\d+)_review\.md")
    versions = [(int(m.group(1)), int(m.group(2))) for f in files if (m := pattern.match(f))]
    
    if versions:
        last_pi, last_spr = max(versions)
        pi_id, sprint_id = last_pi, last_spr + 1
    else:
        pi_id, sprint_id = 1, 1

    # --- GIT SAFETY NET ---
    if not os.path.exists(".git"):
        log("Initializing Git safety net...", C_YELLOW)
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Initial Safety Point"], check=True)

    log(f"FACTORY RESUMED: Starting at {pi_id}.{sprint_id}", C_GREEN, True)
    run_count = 0

    while True:
        if args.max_sprint != -1 and run_count >= args.max_sprint: break
        if os.path.exists("STOP_AGENT.txt"): break
        
        log(f"--- SPRINT {pi_id}.{sprint_id} ---", C_BLUE, True)

        # 1. DEVELOPMENT (Progressive prompt)
        task = "Analyze existing files and implement the next logical feature or UI improvement for Crystal Island."
        resp = run_agent_cli(task, pi_id, sprint_id, "DEV")

        # 2. VERIFY & BACKUP
        success, err = verify_and_deploy(pi_id, sprint_id)
        if not success:
            log("Build Failed. Repairing...", C_RED)
            run_agent_cli(f"FIX BUILD ERROR: {err}", pi_id, sprint_id, "REPAIR")
            success, _ = verify_and_deploy(pi_id, sprint_id)

        # 3. REVIEW LOGGING
        if success:
            review = run_agent_cli("Summarize the progress in 3 bullet points.", pi_id, sprint_id, "REVIEW")

            # Ensure directory exists right before writing
            if not os.path.exists(SPRINT_DIR):
                os.makedirs(SPRINT_DIR)
                log(f"Re-created missing {SPRINT_DIR} folder.", C_YELLOW)

            with open(f"{SPRINT_DIR}/sprint_{pi_id}.{sprint_id}_review.md", "w") as f:
                f.write(str(review))

        sprint_id += 1; run_count += 1; time.sleep(10)

if __name__ == "__main__":
    main()

