param(
    [string]$GrafanaUrl = "http://localhost:3000",
    [string]$InfluxUrl = "http://localhost:8086",
    [string]$InfluxOrg = "comasa",
    [string]$InfluxBucket = "comasa",
    [string]$InfluxToken = "comasa-demo-token",
    [string[]]$Measurements = @("telemetry_raw", "kpi", "anomaly_event", "maintenance_recommendation")
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host "`n==> $Message" -ForegroundColor Cyan
}

function Invoke-Compose {
    param([string[]]$Arguments)
    & docker compose @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "docker compose $($Arguments -join ' ') failed with exit code $LASTEXITCODE"
    }
}

function Invoke-InfluxQuery {
    param([string]$Flux)

    $queryUri = "{0}/api/v2/query?org={1}" -f $InfluxUrl.TrimEnd('/'), [uri]::EscapeDataString($InfluxOrg)
    $headers = @{
        Authorization = "Token $InfluxToken"
        Accept = "application/csv"
    }

    $response = Invoke-WebRequest `
        -Uri $queryUri `
        -Method Post `
        -Headers $headers `
        -ContentType "application/vnd.flux" `
        -Body $Flux `
        -UseBasicParsing `
        -TimeoutSec 15

    return $response.Content
}

function Get-InfluxDataRows {
    param([string]$Csv)

    return @(
        $Csv -split "`r?`n" |
            Where-Object { $_ -and -not $_.StartsWith("#") -and -not $_.StartsWith(",result") }
    )
}

function Get-InfluxLastNumericValue {
    param([string]$Csv)

    $rows = Get-InfluxDataRows -Csv $Csv
    if ($rows.Count -eq 0) {
        return 0
    }

    $lastRow = $rows[-1]
    $lastValue = ($lastRow -split ",")[-1]
    try {
        return [double]::Parse($lastValue, [Globalization.CultureInfo]::InvariantCulture)
    }
    catch {
        return 0
    }
}

Write-Step "Docker Compose service status"
Invoke-Compose -Arguments @("ps")

Write-Step "Grafana health"
$grafanaHealth = Invoke-RestMethod -Uri "$GrafanaUrl/api/health" -TimeoutSec 10
if ($grafanaHealth.database -ne "ok") {
    throw "Grafana health is not ok: $($grafanaHealth | ConvertTo-Json -Compress)"
}
Write-Host "Grafana database: $($grafanaHealth.database), version: $($grafanaHealth.version)"

Write-Step "InfluxDB measurements"
$measurementListFlux = @"
import "influxdata/influxdb/schema"
schema.measurements(bucket: "$InfluxBucket")
"@
$measurementCsv = Invoke-InfluxQuery -Flux $measurementListFlux
$measurementRows = Get-InfluxDataRows -Csv $measurementCsv
$availableMeasurements = @($measurementRows | ForEach-Object { ($_ -split ",")[-1].Trim('"') })

foreach ($measurement in $Measurements) {
    if ($availableMeasurements -notcontains $measurement) {
        throw "InfluxDB measurement '$measurement' was not found in bucket '$InfluxBucket'."
    }
    Write-Host "Found measurement: $measurement"
}

Write-Step "Recent demo data counts (-15m)"
foreach ($measurement in $Measurements) {
    $countFlux = @"
from(bucket: "$InfluxBucket")
  |> range(start: -15m)
  |> filter(fn: (r) => r._measurement == "$measurement")
  |> group()
  |> count(column: "_value")
  |> keep(columns: ["_value"])
"@
    $countCsv = Invoke-InfluxQuery -Flux $countFlux
    $count = Get-InfluxLastNumericValue -Csv $countCsv
    if ($count -le 0) {
        if ($measurement -in @("telemetry_raw", "kpi")) {
            throw "Measurement '$measurement' has no recent rows in the last 15 minutes. Run a scenario for at least 1-2 minutes and re-run this script."
        }

        Write-Warning "Measurement '$measurement' exists but has no recent rows in the last 15 minutes. Run an anomaly scenario to refresh it."
        continue
    }

    Write-Host "Measurement: $measurement, recent rows: $count" -ForegroundColor Yellow
}

Write-Host "`nSmoke check completed successfully." -ForegroundColor Green
