param(
    [int]$DelaySeconds = 20,
    [string]$CommitMessagePrefix = "Auto save"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

$IgnoredPathParts = @(
    "\.git\",
    "\staticfiles\",
    "\__pycache__\",
    "\.venv\",
    "\venv\",
    "\env\"
)

$IgnoredFileNames = @(
    "db.sqlite3"
)

function Test-ShouldIgnorePath {
    param([string]$Path)

    $fullPath = [System.IO.Path]::GetFullPath($Path)
    foreach ($part in $IgnoredPathParts) {
        if ($fullPath -like "*$part*") {
            return $true
        }
    }

    if ($IgnoredFileNames -contains [System.IO.Path]::GetFileName($fullPath)) {
        return $true
    }

    return $false
}

function Invoke-AutoPush {
    $status = git status --short
    if (-not $status) {
        Write-Host "Aucune modification a sauvegarder." -ForegroundColor DarkGray
        return
    }

    Write-Host "Verification Django..." -ForegroundColor Cyan
    python manage.py check
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Verification echouee. Rien n'a ete pousse." -ForegroundColor Red
        return
    }

    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $message = "$CommitMessagePrefix - $timestamp"

    Write-Host "Sauvegarde GitHub: $message" -ForegroundColor Cyan
    git add -A
    if ($LASTEXITCODE -ne 0) {
        Write-Host "git add a echoue." -ForegroundColor Red
        return
    }

    git commit -m $message
    if ($LASTEXITCODE -ne 0) {
        Write-Host "git commit a echoue." -ForegroundColor Red
        return
    }

    git push origin main
    if ($LASTEXITCODE -ne 0) {
        Write-Host "git push a echoue." -ForegroundColor Red
        return
    }

    Write-Host "Modifications envoyees sur GitHub." -ForegroundColor Green
}

$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = $ProjectRoot
$watcher.IncludeSubdirectories = $true
$watcher.EnableRaisingEvents = $true
$watcher.NotifyFilter = [System.IO.NotifyFilters]'FileName, DirectoryName, LastWrite, Size'

$script:PendingChange = $false
$script:LastChangeAt = Get-Date

$action = {
    if (Test-ShouldIgnorePath -Path $Event.SourceEventArgs.FullPath) {
        return
    }

    $script:PendingChange = $true
    $script:LastChangeAt = Get-Date
    Write-Host "Modification detectee: $($Event.SourceEventArgs.FullPath)" -ForegroundColor Yellow
}

$events = @(
    Register-ObjectEvent $watcher Changed -Action $action,
    Register-ObjectEvent $watcher Created -Action $action,
    Register-ObjectEvent $watcher Deleted -Action $action,
    Register-ObjectEvent $watcher Renamed -Action $action
)

Write-Host "Surveillance active. Les changements seront envoyes apres $DelaySeconds secondes sans nouvelle modification." -ForegroundColor Green
Write-Host "Appuie sur Ctrl+C pour arreter." -ForegroundColor Green

try {
    while ($true) {
        Start-Sleep -Seconds 2
        if ($script:PendingChange) {
            $elapsed = ((Get-Date) - $script:LastChangeAt).TotalSeconds
            if ($elapsed -ge $DelaySeconds) {
                $script:PendingChange = $false
                Invoke-AutoPush
            }
        }
    }
}
finally {
    foreach ($event in $events) {
        Unregister-Event -SubscriptionId $event.Id -ErrorAction SilentlyContinue
    }
    $watcher.Dispose()
}
