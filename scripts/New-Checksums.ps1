param(
    [Parameter(Mandatory = $true)]
    [string]$Directory,

    [string]$Version
)

$ErrorActionPreference = "Stop"
$releaseDirectory = (Resolve-Path -LiteralPath $Directory).Path
$outputPath = Join-Path $releaseDirectory "SHA256SUMS.txt"

$files = Get-ChildItem -LiteralPath $releaseDirectory -Filter "*.exe" -File
if ($Version) {
    $expectedNames = @(
        "PADOrganizer-Setup-v$Version.exe",
        "PADOrganizer-portable-v$Version.exe"
    )
    $files = $files | Where-Object { $_.Name -in $expectedNames }
    $missingNames = $expectedNames | Where-Object {
        $_ -notin @($files | ForEach-Object Name)
    }
    if ($missingNames) {
        throw "Missing release files: $($missingNames -join ', ')"
    }
}

$lines = $files |
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
