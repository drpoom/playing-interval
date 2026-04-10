import subprocess
import time
import os
import json

# --- CONFIGURATION ---
SPRINTS_PER_PI = 50  # Set to -1 for infinite mode
AGENT_COMMAND = "openclaw"
DASHBOARD_FILE = "dashboard.json"
STOP_FILE = "STOP_AGENT.txt"
PI_PLANNING_TRIGGER = "START_PI_PLANNING.txt"

def update_dashboard(pi, sprint, status, latest_task="N/A"):
    """Saves system state for the Vue dashboard and OpenClaw reports."""
    data = {
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "pi": pi,
        "sprint": sprint,
        "status": status,
        "latest_task": latest_task,
        "mode": "INFINITE" if SPRINTS_PER_PI == -1 else "BATCHED"
    }
    with open(DASHBOARD_FILE, "w") as f:
        json.dump(data, f, indent=4)

def run_agent(prompt, pi, sprint):
    # We explicitly tell OpenClaw to check the dashboard before replying
    context = (
        f"You are an Agile AI Agent. PI: {pi}, Sprint: {sprint}.\n"
        f"Internal Dashboard state is in {DASHBOARD_FILE}.\n"
        f"TASK: {prompt}\n"
    )
    result = subprocess.run([AGENT_COMMAND, context], capture_output=True, text=True)
    return result.stdout

def main():
    pi_id = 1
    sprint_id = 1
    
    log("Initializing Infinite Agile Loop...")
    
    while True:
        # 1. PI PLANNING CHECK
        # If not infinite (-1), check if we hit the limit. Or check for manual trigger.
        manual_pi = os.path.exists(PI_PLANNING_TRIGGER)
        limit_reached = (SPRINTS_PER_PI != -1 and sprint_id > SPRINTS_PER_PI)
        
        if manual_pi or limit_reached:
            update_dashboard(pi_id, sprint_id, "PI_PLANNING_PAUSE")
            print(f"Waiting for PI Planning...")
            while os.path.exists(PI_PLANNING_TRIGGER):
                time.sleep(10)
            pi_id += 1
            sprint_id = 1
            if manual_pi: os.remove(PI_PLANNING_TRIGGER)

        # 2. SPRINT EXECUTION
        update_dashboard(pi_id, sprint_id, "IMPLEMENTING", "Working on next Vue component")
        run_agent("Perform analysis and implement the next logical feature.", pi_id, sprint_id)

        # 3. VERIFY & DEPLOY
        update_dashboard(pi_id, sprint_id, "VERIFYING", "Running npm test and build")
        # (Assuming your verify/deploy functions from the previous turn are here)
        success = True # Placeholder for logic
        
        # 4. REPORTING (The "Summary" Feature)
        # We prompt the agent specifically to create a channel-friendly summary
        summary = run_agent("Create a 2-sentence summary of what you did this sprint for the human supervisor.", pi_id, sprint_id)
        print(f"CHANNEL SUMMARY: {summary}")

        update_dashboard(pi_id, sprint_id, "COMPLETED", summary)
        
        sprint_id += 1
        time.sleep(2)

if __name__ == "__main__":
    main()
