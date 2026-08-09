param(
    [Parameter(Mandatory = $true)]
    [string]$Directory
)

$ErrorActionPreference = "Stop"
$releaseDirectory = (Resolve-Path -LiteralPath $Directory).Path
$outputPath = Join-Path $releaseDirectory "SHA256SUMS.txt"

$lines = Get-ChildItem -LiteralPath $releaseDirectory -Filter "*.exe" -File |
    Sort-Object Name |
    ForEach-Object {
        $hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
        "$hash  $($_.Name)"
    }

if (-not $lines) {
    throw "No .exe files were found in $releaseDirectory"
}

[System.IO.File]::WriteAllLines(
    $outputPath,
    [string[]]$lines,
    [System.Text.UTF8Encoding]::new($false)
)

Write-Host "Created $outputPath"
