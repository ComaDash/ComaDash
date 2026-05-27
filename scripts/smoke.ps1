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

function Split-CsvLine {
    param([string]$Line)

    $fields = New-Object System.Collections.Generic.List[string]
    $current = New-Object System.Text.StringBuilder
    $inQuotes = $false

    for ($i = 0; $i -lt $Line.Length; $i++) {
        $char = $Line[$i]

        if ($char -eq '"') {
            if ($inQuotes -and ($i + 1) -lt $Line.Length -and $Line[$i + 1] -eq '"') {
                [void]$current.Append('"')
                $i++
                continue
            }

            $inQuotes = -not $inQuotes
            continue
        }

        if ($char -eq ',' -and -not $inQuotes) {
            $fields.Add($current.ToString()) | Out-Null
            [void]$current.Clear()
            continue
        }

        [void]$current.Append($char)
    }

    $fields.Add($current.ToString()) | Out-Null
    return @($fields.ToArray())
}

function ConvertFrom-InfluxAnnotatedCsv {
    param([string]$Csv)

    $headers = $null
    $records = @()

    foreach ($line in ($Csv -split "`r?`n")) {
        if ([string]::IsNullOrWhiteSpace($line) -or $line.StartsWith("#")) {
            continue
        }

        $fields = @(Split-CsvLine -Line $line)
        if ($fields.Count -eq 0) {
            continue
        }

        if ($fields -contains "result" -and $fields -contains "table" -and $fields -contains "_value") {
            $headers = @($fields)
            continue
        }

        if ($null -eq $headers) {
            continue
        }

        $record = [ordered]@{}
        for ($i = 0; $i -lt $headers.Count; $i++) {
            $name = $headers[$i]
            if ([string]::IsNullOrWhiteSpace($name)) {
                $name = "_annotation"
            }
            elseif ($record.Contains($name)) {
                $name = "{0}_{1}" -f $name, $i
            }

            $value = $null
            if ($i -lt $fields.Count) {
                $value = $fields[$i]
            }

            $record[$name] = $value
        }

        $records += [pscustomobject]$record
    }

    return $records
}

function Get-InfluxColumnValues {
    param(
        [string]$Csv,
        [string]$ColumnName = "_value"
    )

    $records = ConvertFrom-InfluxAnnotatedCsv -Csv $Csv
    return @(
        foreach ($record in $records) {
            if ($record.PSObject.Properties.Name -contains $ColumnName) {
                $record.$ColumnName
            }
        }
    )
}

function Get-InfluxLastNumericValue {
    param([string]$Csv)

    $values = @(Get-InfluxColumnValues -Csv $Csv -ColumnName "_value")
    if ($values.Count -eq 0) {
        return 0
    }

    $lastValue = $values[-1]
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
$availableMeasurements = Get-InfluxColumnValues -Csv $measurementCsv -ColumnName "_value"

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
  |> yield(name: "count")
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
