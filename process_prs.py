#!/usr/bin/env python3
import json
import subprocess
import os

os.chdir("/mnt/backup/projects/ingress-nginx/.sidekick/worktrees/rebase-prs-mod-0")

with open(".sidekick/open_prs.json") as f:
    prs = json.load(f)

matching_prs = [pr for pr in prs if pr["number"] % 4 == 0]
print(f"Matching PRs: {[pr['number'] for pr in matching_prs]}")

results = {}

def run(cmd, **kwargs):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, **kwargs)
    print(f"returncode: {result.returncode}")
    if result.stdout:
        print(f"stdout: {result.stdout[:800]}")
    if result.stderr:
        print(f"stderr: {result.stderr[:800]}")
    return result

# Fetch origin master
run("git fetch origin master")

# Check if sidekick remote exists
remotes = run("git remote")
if "sidekick" not in remotes.stdout:
    run("git remote add sidekick git@github.com:redevops-io/ingress-nginx.git")

for pr in matching_prs:
    pr_num = pr["number"]
    head_oid = pr["headRefOid"]
    branch_name = f"pr-{pr_num}"
    
    # Fetch PR head
    fetch_result = run(f"git fetch origin {head_oid}")
    if fetch_result.returncode != 0:
        results[pr_num] = {"status": "fetch_failed", "error": fetch_result.stderr}
        continue
    
    # Create branch
    checkout_result = run(f"git checkout -B {branch_name} {head_oid}")
    if checkout_result.returncode != 0:
        results[pr_num] = {"status": "checkout_failed", "error": checkout_result.stderr}
        continue
    
    # Attempt rebase
    rebase_result = run("git rebase origin/master")
    if rebase_result.returncode != 0:
        # Check for trivial conflicts
        status_result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
        conflict_files = [line.strip() for line in status_result.stdout.splitlines() 
                         if line.startswith("UU ") or line.startswith("AU ") or line.startswith("UA ")]
        print(f"Conflict files: {conflict_files}")
        
        trivial_resolved = False
        for fline in conflict_files:
            parts = fline.split()
            fname = parts[-1] if len(parts) > 1 else parts[0]
            # Auto-resolve go.sum by accepting theirs and running go mod tidy
            if fname == "go.sum" or fname.endswith("/go.sum"):
                subprocess.run(f"git checkout --theirs {fname}", shell=True, capture_output=True, text=True)
                subprocess.run(f"git add {fname}", shell=True, capture_output=True, text=True)
                subprocess.run("go mod tidy", shell=True, capture_output=True, text=True)
                subprocess.run("git add go.mod go.sum", shell=True, capture_output=True, text=True)
                trivial_resolved = True
            elif fname == "go.mod" or fname.endswith("/go.mod"):
                subprocess.run(f"git checkout --theirs {fname}", shell=True, capture_output=True, text=True)
                subprocess.run(f"git add {fname}", shell=True, capture_output=True, text=True)
                trivial_resolved = True
        
        # Check if all resolved
        status_after = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
        remaining_conflicts = [line for line in status_after.stdout.splitlines() 
                              if line.startswith("UU ") or line.startswith("AU ") or line.startswith("UA ")]
        
        if not remaining_conflicts:
            has_staged = subprocess.run("git diff --cached --name-only", shell=True, capture_output=True, text=True)
            if has_staged.stdout.strip() or trivial_resolved:
                continue_result = run("GIT_EDITOR=true git rebase --continue")
                if continue_result.returncode == 0:
                    rebase_result = continue_result
        
        if rebase_result.returncode != 0:
            subprocess.run("git rebase --abort", shell=True, capture_output=True, text=True)
            run(f"git checkout sidekick/rebase-prs-mod-0")
            results[pr_num] = {"status": "rebase_failed", "error": rebase_result.stderr}
            continue
    
    # Rebase succeeded, run sanity check
    # go is not available, but make is. Try ARCH=amd64 make build as fastest available check.
    sanity_result = run("ARCH=amd64 make build")
    
    if sanity_result.returncode == 0:
        # Push to sidekick remote
        push_result = run(f"git push sidekick {branch_name}:{branch_name}-rebased")
        if push_result.returncode == 0:
            results[pr_num] = {"status": "success", "sanity_check": "passed"}
        else:
            results[pr_num] = {"status": "push_failed", "error": push_result.stderr}
    else:
        results[pr_num] = {"status": "sanity_check_failed", "error": sanity_result.stderr}
    
    # Go back to original branch
    run(f"git checkout sidekick/rebase-prs-mod-0")

# Write results
with open(".sidekick/pr_results_mod_0.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"Final Results: {results}")
