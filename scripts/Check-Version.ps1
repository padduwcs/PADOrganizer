param(
    [Parameter(Mandatory = $true)]
    [string]$ExpectedVersion
)

$ErrorActionPreference = "Stop"
$versionFile = Join-Path $PSScriptRoot "..\version.py"
$content = Get-Content -LiteralPath $versionFile -Raw -Encoding UTF8
$match = [regex]::Match($content, '(?m)^APP_VERSION\s*=\s*"(\d+\.\d+\.\d+)"\s*$')

if (-not $match.Success) {
    throw "Cannot read APP_VERSION from version.py"
}

$sourceVersion = $match.Groups[1].Value
if ($sourceVersion -ne $ExpectedVersion) {
    throw "Version mismatch: version.py is $sourceVersion but the requested release is $ExpectedVersion"
}

Write-Host "Version check passed: $sourceVersion"
