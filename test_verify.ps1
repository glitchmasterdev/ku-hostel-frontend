$ErrorActionPreference = 'Stop'

Write-Host "=== Testing Landing Page ==="
$r = Invoke-WebRequest -Uri 'http://localhost:3000' -UseBasicParsing
Write-Host "Status: $($r.StatusCode)"
Write-Host "Size: $($r.Content.Length) bytes"
$c = $r.Content
if ($c -like '*hero-section*') { Write-Host 'PASS: Hero section found' } else { Write-Host 'FAIL: Hero section missing' }
if ($c -like '*features-grid*') { Write-Host 'PASS: Features grid found' } else { Write-Host 'FAIL: Features grid missing' }
if ($c -like '*Apply for Hostel*') { Write-Host 'PASS: Apply button found' } else { Write-Host 'FAIL: Apply button missing' }
if ($c -like '*styles.css*') { Write-Host 'PASS: Custom CSS linked' } else { Write-Host 'FAIL: Custom CSS missing' }
if ($c -like '*footer*') { Write-Host 'PASS: Footer found' } else { Write-Host 'FAIL: Footer missing' }

Write-Host ""
Write-Host "=== Testing Allocation Page ==="
$r2 = Invoke-WebRequest -Uri 'http://localhost:3000/allocation.php' -UseBasicParsing
Write-Host "Status: $($r2.StatusCode)"
$c2 = $r2.Content
if ($c2 -like '*allocation-form*') { Write-Host 'PASS: Allocation form found' } else { Write-Host 'FAIL: Allocation form missing' }
if ($c2 -like '*reg_no*') { Write-Host 'PASS: reg_no input found' } else { Write-Host 'FAIL: reg_no input missing' }

Write-Host ""
Write-Host "=== Testing API - Valid Student ==="
$body = '{"reg_no": "J17/1234/2026"}'
$r3 = Invoke-WebRequest -Uri 'http://localhost:3000/api/check-allocation' -Method POST -Body $body -ContentType 'application/json' -UseBasicParsing
Write-Host "Response: $($r3.Content)"

Write-Host ""
Write-Host "=== Testing API - Invalid Student ==="
$body2 = '{"reg_no": "INVALID/NUMBER"}'
$r4 = Invoke-WebRequest -Uri 'http://localhost:3000/api/check-allocation' -Method POST -Body $body2 -ContentType 'application/json' -UseBasicParsing
Write-Host "Response: $($r4.Content)"

Write-Host ""
Write-Host "=== Testing CSS File ==="
$r5 = Invoke-WebRequest -Uri 'http://localhost:3000/css/styles.css' -UseBasicParsing
Write-Host "Status: $($r5.StatusCode)"
Write-Host "CSS Size: $($r5.Content.Length) bytes"
if ($r5.Content -like '*--ku-navy*') { Write-Host 'PASS: Design tokens found' } else { Write-Host 'FAIL: Design tokens missing' }

Write-Host ""
Write-Host "=== All tests complete ==="
