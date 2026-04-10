import subprocess
import time
import os
import sys
import json
import re
import argparse

# --- CONFIGURATION ---
PROJECT_DIR = "."
AGENT_COMMAND = ["openclaw", "chat", "--workspace", "."] 
GOAL_FILE = "goal.md"
SPRINT_DIR = "./sprints"
DASHBOARD_FILE = "dashboard.json"
STOP_FILE = "STOP_AGENT.txt"
PI_PLANNING_TRIGGER = "START_PI_PLANNING.txt"

def log(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def get_latest_version():
    if not os.path.exists(SPRINT_DIR):
        os.makedirs(SPRINT_DIR)
        return 1, 0
    files = os.listdir(SPRINT_DIR)
    pattern = re.compile(r"sprint_(\d+)\.(\d+)_review\.md")
    versions = []
    for f in files:
        match = pattern.match(f)
        if match:
            versions.append((int(match.group(1)), int(match.group(2))))
    if not versions:
        return 1, 0
    versions.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return versions[0]

def update_dashboard(pi, sprint, status, latest_task="N/A"):
    data = {
        "project": "The Myth of Crystal Island",
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "pi": pi, "sprint": sprint, "status": status, "latest_task": latest_task
    }
    with open(DASHBOARD_FILE, "w") as f:
        json.dump(data, f, indent=4)

def run_agent(prompt, pi, sprint, step_name="STEP"):
    if not os.path.exists(GOAL_FILE):
        log(f"[ERROR] {GOAL_FILE} missing!")
        return ""
    with open(GOAL_FILE, "r") as f:
        goal = f.read()
    
    full_prompt = (
        f"--- INSTRUCTIONS FOR SPRINT {pi}.{sprint} ---\n"
        f"PROJECT GOAL: {goal}\n"
        f"CURRENT TASK: {prompt}\n"
        f"IMPORTANT: Respond with content only. For reviews, use 3 bullet points."
    )
    
    log(f"[DEBUG] Starting Agent: {step_name}")
    cmd = AGENT_COMMAND + [full_prompt]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.stdout.strip():
            print(f"\n--- [AGENT STDOUT: {step_name}] ---\n{result.stdout.strip()}\n---")
        if result.stderr.strip():
            print(f"\n!!! [AGENT STDERR: {step_name}] !!!\n{result.stderr.strip()}\n---")
        return result.stdout.strip() if result.returncode == 0 else ""
    except Exception as e:
        log(f"[ERROR] Agent failed: {e}")
        return ""

def verify_and_deploy(pi, sprint):
    log(f"--- VERIFYING SPRINT {pi}.{sprint} ---")
    build = subprocess.run(["npm", "run", "build"], capture_output=True, text=True)
    if build.returncode != 0: return False, build.stderr

    test = subprocess.run(["npm", "test"], capture_output=True, text=True)
    if test.returncode != 0: return False, test.stdout

    try:
        subprocess.run(["git", "add", "."], check=True)
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if status.stdout.strip():
            subprocess.run(["git", "commit", "-m", f"Auto-Deploy: PI {pi} Sprint {sprint}"], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            log("Git push successful.")
        return True, ""
    except Exception as e:
        log(f"[ERROR] Git failed: {e}")
        return False, "Git Failure"

def main():
    parser = argparse.ArgumentParser(description="The Myth of Crystal Island Driver")
    parser.add_argument("--pi", type=int, help="Starting PI")
    parser.add_argument("--sprint", type=int, help="Starting Sprint")
    parser.add_argument("--max-sprint", type=int, default=-1, help="Max sprints to run (-1 for infinite)")
    args = parser.parse_args()

    last_pi, last_sprint = get_latest_version()
    pi_id = args.pi if args.pi is not None else last_pi
    sprint_id = args.sprint if args.sprint is not None else last_sprint + 1
    
    # Track how many sprints we've completed in THIS session
    sprints_completed_this_session = 0

    log(f"DRIVER STARTING: PI {pi_id}, Sprint {sprint_id} (Max: {args.max_sprint})")

    while True:
        # Check Stop Signals
        if os.path.exists(STOP_FILE):
            log("Stop file detected. Exiting."); break
        
        # Check Session Limit
        if args.max_sprint != -1 and sprints_completed_this_session >= args.max_sprint:
            log(f"Reached max sprint limit ({args.max_sprint}). Shutting down gracefully.")
            break

        # Check PI Planning Trigger
        if os.path.exists(PI_PLANNING_TRIGGER):
            update_dashboard(pi_id, sprint_id, "PAUSED_FOR_PI_PLANNING")
            log("Paused for PI Planning. Delete trigger file to resume.")
            while os.path.exists(PI_PLANNING_TRIGGER): time.sleep(10)
            pi_id += 1
            sprint_id = 1

        log(f"\n==== STARTING SPRINT {pi_id}.{sprint_id} ====")

        # 1. IMPLEMENT
        update_dashboard(pi_id, sprint_id, "DEVELOPING")
        run_agent("Implement the next part of the story/logic in the Vue project.", pi_id, sprint_id, "IMPLEMENTATION")

        # 2. VERIFY
        update_dashboard(pi_id, sprint_id, "VERIFYING")
        success, logs = verify_and_deploy(pi_id, sprint_id)
        if not success:
            log("Failed. Repairing...")
            run_agent(f"REPAIR: Fix these errors:\n{logs}", pi_id, sprint_id, "REPAIR")
            success, _ = verify_and_deploy(pi_id, sprint_id)

        # 3. REVIEW
        update_dashboard(pi_id, sprint_id, "REVIEWING")
        review = run_agent("Summarize work in 3 short bullet points.", pi_id, sprint_id, "REVIEW")
        
        review_filename = f"{SPRINT_DIR}/sprint_{pi_id}.{sprint_id}_review.md"
        with open(review_filename, "w") as f:
            f.write(review if review else "# Review Error")
        
        log(f"Sprint {pi_id}.{sprint_id} Complete.")
        
        sprint_id += 1
        sprints_completed_this_session += 1
        time.sleep(5)

if __name__ == "__main__":
    main()

