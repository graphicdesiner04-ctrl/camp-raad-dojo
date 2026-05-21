# Auto-commit and push changes to GitHub
# Called by Claude Code PostToolUse hook after Edit/Write

$json = $input | ConvertFrom-Json
$fp = $json.tool_input.file_path

# Only act on files inside this repo
$repoDir = "G:\claude\Website el Waleed"
if (-not $fp -or -not $fp.StartsWith($repoDir)) { exit 0 }

Set-Location $repoDir

# Stage, commit, push
git add "$fp" 2>$null
$status = git status --porcelain "$fp" 2>$null
if (-not $status) { exit 0 }   # nothing to commit

git commit -m "auto: update $fname" 2>$null
git push 2>$null
