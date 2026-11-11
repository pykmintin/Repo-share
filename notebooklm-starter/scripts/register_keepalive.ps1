# Optional Windows Task Scheduler setup. Requires explicit owner approval.
# Tasks use the signed-in Windows account, do not contain Google credentials,
# and cannot refresh while signed out, powered off, or without network.
[CmdletBinding()]
param(
    [ValidatePattern('^[A-Za-z][A-Za-z0-9_-]{0,31}$')]
    [string]$Profile = 'personal',
    [ValidateRange(15, 60)]
    [int]$Minutes = 20,
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$project = Split-Path -Parent $PSScriptRoot
$venvPython = Join-Path $project '.venv\Scripts\python.exe'
$runner = Join-Path $PSScriptRoot 'refresh.py'
$notebookHome = if ($env:NOTEBOOKLM_HOME) { $env:NOTEBOOKLM_HOME } else { Join-Path $env:USERPROFILE '.notebooklm' }
$storage = Join-Path $notebookHome "profiles\$Profile\storage_state.json"
$name = "NotebookLM-Starter-$Profile"

if (-not (Test-Path -LiteralPath $venvPython -PathType Leaf)) {
    throw 'No local Python environment; run python scripts/bootstrap.py install first.'
}
if (-not (Test-Path -LiteralPath $storage -PathType Leaf)) {
    throw "No saved session for profile '$Profile'. Authenticate and verify it first."
}
if (Get-ScheduledTask -TaskName $name -ErrorAction SilentlyContinue) {
    throw "The task '$name' already exists. Review it instead of overwriting."
}

$identity = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
if ($DryRun) {
    Write-Output "DRY_RUN task=$name user=$identity interval=$Minutes profile=$Profile"
    exit 0
}
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(3) -RepetitionInterval (New-TimeSpan -Minutes $Minutes) -RepetitionDuration (New-TimeSpan -Days 3650)
$action = New-ScheduledTaskAction -Execute $venvPython -Argument ("`"" + $runner + "`" --profile " + $Profile)
$principal = New-ScheduledTaskPrincipal -UserId $identity -LogonType Interactive -RunLevel Limited
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 3)
$null = Register-ScheduledTask -TaskName $name -Description "Approved, per-profile NotebookLM auth cookie refresh; no embedded credentials." -Action $action -Trigger $trigger -Principal $principal -Settings $settings
$installed = Get-ScheduledTask -TaskName $name
if ($installed.Actions[0].Arguments -notlike "*--profile $Profile") {
    throw "Task definition did not preserve the selected profile."
}
Write-Output "REGISTERED task=$name refresh_every=$Minutes-minutes (requires Windows user logged in)"
