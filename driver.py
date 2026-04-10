import subprocess
import time
import os
import sys
import json
import re
import argparse

# --- CONFIGURATION ---
PROJECT_DIR = "."
AGENT_COMMAND = "openclaw" # Ensure this is in your PATH
GOAL_FILE = "goal.md"
SPRINT_DIR = "./sprints"
DASHBOARD_FILE = "dashboard.json"
STOP_FILE = "STOP_AGENT.txt"
PI_PLANNING_TRIGGER = "START_PI_PLANNING.txt"

def log(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def get_latest_version():
    """
    Scans the sprints directory for sprint_x.y_review.md 
    and returns the latest (PI, Sprint) as integers.
    """
    if not os.path.exists(SPRINT_DIR):
        os.makedirs(SPRINT_DIR)
        return 1, 0 # Start from PI 1, Sprint 0 (so next is 1.1)

    files = os.listdir(SPRINT_DIR)
    # Pattern to match sprint_PI.SPRINT_review.md
    pattern = re.compile(r"sprint_(\d+)\.(\d+)_review\.md")
    
    versions = []
    for f in files:
        match = pattern.match(f)
        if match:
            versions.append((int(match.group(1)), int(match.group(2))))
    
    if not versions:
        return 1, 0
    
    # Sort by PI first, then Sprint
    versions.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return versions[0]

def update_dashboard(pi, sprint, status, latest_task="N/A"):
    data = {
        "project": "The Myth of Crystal Island",
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "pi": pi,
        "sprint": sprint,
        "status": status,
        "latest_task": latest_task
    }
    with open(DASHBOARD_FILE, "w") as f:
        json.dump(data, f, indent=4)

def run_agent(prompt, pi, sprint):
    with open(GOAL_FILE, "r") as f:
        goal = f.read()
    
    full_prompt = (
        f"--- AGILE CONTEXT ---\n"
        f"PROJECT: The Myth of Crystal Island\n"
        f"PI: {pi} | SPRINT: {sprint}\n"
        f"VISION: {goal}\n\n"
        f"TASK: {prompt}"
    )
    # Using subprocess to call the agent CLI
    result = subprocess.run([AGENT_COMMAND, full_prompt], capture_output=True, text=True)
    return result.stdout

def verify_and_deploy(pi, sprint):
    log("Verifying Vue Build...")
    build = subprocess.run(["npm", "run", "build"], capture_output=True, text=True)
    if build.returncode != 0:
        return False, build.stderr

    log("Running Tests...")
    test = subprocess.run(["npm", "test"], capture_output=True, text=True)
    if test.returncode != 0:
        return False, test.stdout

    # Git Push
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", f"Sprint {pi}.{sprint} Complete"])
    subprocess.run(["git", "push", "origin", "main"])
    return True, ""

def main():
    parser = argparse.ArgumentParser(description="The Myth of Crystal Island: Agile Driver")
    parser.add_argument("--pi", type=int, help="Manual PI override")
    parser.add_argument("--sprint", type=int, help="Manual Sprint override")
    args = parser.parse_args()

    # Determine start state
    if args.pi is not None and args.sprint is not None:
        pi_id, sprint_id = args.pi, args.sprint
        log(f"Manual Start: PI {pi_id}, Sprint {sprint_id}")
    else:
        last_pi, last_sprint = get_latest_version()
        pi_id = last_pi
        sprint_id = last_sprint + 1
        log(f"Auto-Detected: Resuming from PI {pi_id}, Sprint {sprint_id}")

    while True:
        # Check Stop Signals
        if os.path.exists(STOP_FILE):
            log("Stop file detected. Exiting..."); break
        
        if os.path.exists(PI_PLANNING_TRIGGER):
            update_dashboard(pi_id, sprint_id, "PI_PLANNING_PAUSED")
            log("PI Planning Triggered. Waiting for human intervention...")
            while os.path.exists(PI_PLANNING_TRIGGER):
                time.sleep(10)
            # Reset logic for new PI if the user manual incremented or changed goal
            pi_id += 1
            sprint_id = 1
            log(f"Resuming with PI {pi_id}")

        log(f"\n--- SPRINT {pi_id}.{sprint_id} START ---")
        
        # 1. Implementation
        update_dashboard(pi_id, sprint_id, "DEVELOPING")
        run_agent("Continue the prologue implementation. Fix any bugs and add features per story.md.", pi_id, sprint_id)

        # 2. Verification
        update_dashboard(pi_id, sprint_id, "VERIFYING")
        success, logs = verify_and_deploy(pi_id, sprint_id)
        
        if not success:
            log("Sprint failed verification. Attempting one-shot repair...")
            run_agent(f"REPAIR TASK: The build/test failed with these logs:\n{logs}", pi_id, sprint_id)
            success, _ = verify_and_deploy(pi_id, sprint_id)

        # 3. Sprint Review & Persistence
        review = run_agent("Generate a short summary of accomplishments for this sprint.", pi_id, sprint_id)
        review_filename = f"{SPRINT_DIR}/sprint_{pi_id}.{sprint_id}_review.md"
        with open(review_filename, "w") as f:
            f.write(review)
        
        update_dashboard(pi_id, sprint_id, "SUCCESS", review[:50] + "...")
        
        log(f"Sprint {pi_id}.{sprint_id} finished successfully.")
        
        sprint_id += 1
        time.sleep(5)

if __name__ == "__main__":
    main()

