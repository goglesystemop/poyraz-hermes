[CmdletBinding(PositionalBinding = $false)]
param(
    [string]$DataHome = 'C:\PoyrazAI\hermes-state',
    [string]$ToolHome = (Join-Path $PSScriptRoot '../../poyraz-hermes-tools'),
    [Parameter(ValueFromRemainingArguments = $true)][string[]]$HermesArgs
)
$ErrorActionPreference = 'Stop'
$checkout = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).ProviderPath.Replace('/', '\').TrimEnd('\')
$digest = [System.Security.Cryptography.SHA256]::HashData([System.Text.Encoding]::UTF8.GetBytes($checkout))
$installKey = [Convert]::ToHexString($digest).ToLowerInvariant().Substring(0, 16)
$factsPath = Join-Path $DataHome "installs/$installKey/facts.json"
if (-not (Test-Path -LiteralPath $factsPath)) {
    throw 'This checkout has no completed PM installation in DataHome. Run setup-hermes.ps1 with the same HERMES_HOME and HERMES_RUNTIME_DIR first.'
}
$facts = Get-Content -LiteralPath $factsPath -Raw | ConvertFrom-Json
$interpreter = Join-Path $facts.packages.venv.environment 'Scripts/python.exe'
if (-not (Test-Path -LiteralPath $interpreter)) { throw 'The PM-managed interpreter is missing. Repair the installation before starting.' }
$saved = @{}
foreach ($name in @('HERMES_HOME', 'HERMES_RUNTIME_DIR', 'PYTHONPATH')) {
    $saved[$name] = [Environment]::GetEnvironmentVariable($name)
}
try {
    $env:HERMES_HOME = [System.IO.Path]::GetFullPath($DataHome)
    $env:HERMES_RUNTIME_DIR = [System.IO.Path]::GetFullPath($ToolHome)
    $env:PYTHONPATH = $checkout
    & $interpreter (Join-Path $checkout 'hermes') @HermesArgs
    $result = $LASTEXITCODE
} finally {
    foreach ($name in $saved.Keys) {
        if ($null -eq $saved[$name]) { Remove-Item "env:$name" -ErrorAction SilentlyContinue }
        else { Set-Item "env:$name" $saved[$name] }
    }
}
exit $result
