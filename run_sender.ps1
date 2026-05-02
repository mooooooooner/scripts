param(
    [Parameter(Mandatory = $true)]
    [string]$Endpoint,
    [double]$Timeout = 10
)

$ErrorActionPreference = "Stop"
$senderUrl = if ($env:SENDER_URL) {
    $env:SENDER_URL
} else {
    "https://raw.githubusercontent.com/mooooooooner/scripts/main/sender.py"
}

$tmpDir = Join-Path $env:TEMP ("sender-" + [Guid]::NewGuid().ToString("N"))
$senderPath = Join-Path $tmpDir "sender.py"

New-Item -ItemType Directory -Path $tmpDir | Out-Null

try {
    Invoke-WebRequest -UseBasicParsing -Uri $senderUrl -OutFile $senderPath

    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
    if (-not $pythonCmd) {
        throw "python not found in PATH."
    }

    & $pythonCmd.Source $senderPath --endpoint $Endpoint --timeout $Timeout
    exit $LASTEXITCODE
}
finally {
    Remove-Item -LiteralPath $tmpDir -Recurse -Force -ErrorAction SilentlyContinue
}
