import subprocess
import time
import os
import sys
import json
import re
import argparse

# --- CONFIGURATION ---
PROJECT_DIR = "."
# We use 'chat' as the subcommand to ensure OpenClaw treats the prompt as a message
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
    """Scans the sprints folder for the highest x.y version."""
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
    """Runs the agent and captures output with full debug visibility."""
    if not os.path.exists(GOAL_FILE):
        log(f"[ERROR] {GOAL_FILE} missing! Agent cannot proceed.")
        return ""

    with open(GOAL_FILE, "r") as f:
        goal = f.read()
    
    # We explicitly label this as a task to prevent OpenClaw from misparsing CLI flags
    full_prompt = (
        f"--- INSTRUCTIONS FOR SPRINT {pi}.{sprint} ---\n"
        f"PROJECT GOAL: {goal}\n"
        f"CURRENT TASK: {prompt}\n"
        f"IMPORTANT: Please respond with content only. If this is a review, provide 3 bullet points."
    )
    
    log(f"[DEBUG] Starting Agent: {step_name}")
    
    # Build the full command list
    cmd = AGENT_COMMAND + [full_prompt]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300) # 5 min timeout
        
        # Log Agent behavior
        if result.stdout.strip():
            print(f"\n--- [AGENT STDOUT: {step_name}] ---\n{result.stdout.strip()}\n---")
        if result.stderr.strip():
            print(f"\n!!! [AGENT STDERR: {step_name}] !!!\n{result.stderr.strip()}\n---")
            
        if result.returncode != 0:
            log(f"[ERROR] Agent failed (Code {result.returncode}). Step: {step_name}")
            return ""

        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        log(f"[ERROR] Agent timed out during {step_name}")
        return ""
    except Exception as e:
        log(f"[ERROR] Unexpected error running agent: {e}")
        return ""

def verify_and_deploy(pi, sprint):
    """Checks build, runs tests, and pushes to GitHub."""
    log(f"--- VERIFYING SPRINT {pi}.{sprint} ---")
    
    # 1. Build Check
    log("Building Vue project (npm run build)...")
    build = subprocess.run(["npm", "run", "build"], capture_output=True, text=True)
    if build.returncode != 0:
        log("[FAIL] Build failed.")
        return False, build.stderr

    # 2. Test Check
    log("Running Vitest (npm test)...")
    test = subprocess.run(["npm", "test"], capture_output=True, text=True)
    if test.returncode != 0:
        log("[FAIL] Tests failed.")
        return False, test.stdout

    # 3. Git Deploy
    log("[SUCCESS] Build and Tests passed. Deploying...")
    try:
        subprocess.run(["git", "add", "."], check=True)
        # Check if there are actually changes to commit
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if status.stdout.strip():
            subprocess.run(["git", "commit", "-m", f"Auto-Deploy: PI {pi} Sprint {sprint}"], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            log("Git push successful.")
        else:
            log("No changes detected. Skipping commit.")
        return True, ""
    except subprocess.CalledProcessError as e:
        log(f"[ERROR] Git operation failed: {e}")
        return False, "Git Push Failure"

def main():
    parser = argparse.ArgumentParser(description="The Myth of Crystal Island Driver")
    parser.add_argument("--pi", type=int)
    parser.add_argument("--sprint", type=int)
    args = parser.parse_args()

    # Determine Start State
    last_pi, last_sprint = get_latest_version()
    pi_id = args.pi if args.pi is not None else last_pi
    sprint_id = args.sprint if args.sprint is not None else last_sprint + 1

    log(f"DRIVER STARTING: Target PI {pi_id}, Sprint {sprint_id}")

    while True:
        # Check for manual stop
        if os.path.exists(STOP_FILE):
            log("Stop file detected. Shutting down."); break
        
        # Check for PI Planning break
        if os.path.exists(PI_PLANNING_TRIGGER):
            update_dashboard(pi_id, sprint_id, "PAUSED_FOR_PI_PLANNING")
            log("Paused for PI Planning. Delete the trigger file to resume.")
            while os.path.exists(PI_PLANNING_TRIGGER):
                time.sleep(10)
            pi_id += 1
            sprint_id = 1
            log(f"Beginning New PI: {pi_id}")

        log(f"\n==== STARTING SPRINT {pi_id}.{sprint_id} ====")

        # 1. IMPLEMENTATION
        update_dashboard(pi_id, sprint_id, "DEVELOPING")
        run_agent("Implement the next part of the story/logic in the Vue project.", pi_id, sprint_id, "IMPLEMENTATION")

        # 2. VERIFICATION
        update_dashboard(pi_id, sprint_id, "VERIFYING")
        success, logs = verify_and_deploy(pi_id, sprint_id)
        
        if not success:
            log("Verification failed. Sending logs to agent for one-shot repair...")
            run_agent(f"REPAIR: The project failed to build/test. Fix these errors:\n{logs}", pi_id, sprint_id, "REPAIR")
            success, _ = verify_and_deploy(pi_id, sprint_id)

        # 3. REVIEW
        update_dashboard(pi_id, sprint_id, "GENERATING_REVIEW")
        review = run_agent("Summarize your work this sprint in 3 short bullet points.", pi_id, sprint_id, "REVIEW")
        
        if not review:
            review = "# Review Error\nAgent failed to respond during review generation phase."
            log("[WARNING] Empty review generated.")

        # Save Review File
        review_filename = f"{SPRINT_DIR}/sprint_{pi_id}.{sprint_id}_review.md"
        with open(review_filename, "w") as f:
            f.write(review)
        
        log(f"Sprint {pi_id}.{sprint_id} Complete. Review saved.")
        update_dashboard(pi_id, sprint_id, "IDLE_PENDING_NEXT")
        
        sprint_id += 1
        time.sleep(5)

if __name__ == "__main__":
    main()

