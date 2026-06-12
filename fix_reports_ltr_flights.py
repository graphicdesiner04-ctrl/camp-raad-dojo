import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'G:\claude\Website el Waleed\camp-dashboard.html'
with open(path, encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 1. Fix _reportPage: make direction & th alignment dynamic
# ============================================================
old_reportPage_body = (
    "body{font-family:'Cairo',Arial,sans-serif;background:#fff;color:#1a2332;direction:rtl;font-size:13px}\n"
    "table{width:100%;border-collapse:collapse}\n"
    "th{background:#0f1c2e;color:#fff;padding:10px 12px;text-align:right;font-size:12px;font-weight:600;white-space:nowrap}\n"
    "td{padding:9px 12px;border-bottom:1px solid #e2e8f0;vertical-align:middle}\n"
    "tr:nth-child(even) td{background:#f8fafc}\n"
    "tr:hover td{background:#f0f4ff}"
)

new_reportPage_body = (
    "body{font-family:'Cairo',Arial,sans-serif;background:#fff;color:#1a2332;direction:${dir};font-size:13px}\n"
    "table{width:100%;border-collapse:collapse}\n"
    "th{background:#0f1c2e;color:#fff;padding:10px 12px;text-align:${thAlign};font-size:12px;font-weight:600;white-space:nowrap}\n"
    "td{padding:9px 12px;border-bottom:1px solid #e2e8f0;vertical-align:middle}\n"
    "tr:nth-child(even) td{background:#f8fafc}\n"
    "tr:hover td{background:#f0f4ff}"
)

if old_reportPage_body not in content:
    print('ERROR: _reportPage CSS block not found')
    exit(1)

content = content.replace(old_reportPage_body, new_reportPage_body, 1)

# Also add thAlign variable declaration right after the dir= line inside _reportPage
old_dir_line = "  const dir=lang==='ar'?'rtl':'ltr';\n  return"
new_dir_line = "  const dir=lang==='ar'?'rtl':'ltr';\n  const thAlign=lang==='ar'?'right':'left';\n  return"

if old_dir_line not in content:
    print('ERROR: dir line not found in _reportPage')
    exit(1)

content = content.replace(old_dir_line, new_dir_line, 1)

print('_reportPage fix done')

# ============================================================
# 2. Fix _buildFlightsReport: add flight number columns
# ============================================================

# Replace the rows mapping to include flight numbers
old_rows = """  const rows = sortedP.map((p,i)=>`<tr>
    <td style="text-align:center">${i+1}</td>
    <td><b>${isAr?p.arabicName:(p.englishName||p.arabicName)}</b></td>
    <td>${p.nationality||'—'}</td>
    <td dir="ltr">${p.phone||'—'}</td>
    <td><code>${p.passportNumber||'—'}</code></td>
    <td>${p.departureDateTrip||'—'}</td>
    <td>${p.departureTimeTrip||'—'}</td>
    <td>${p.returnDateTrip||'—'}</td>
    <td>${p.returnTimeTrip||'—'}</td>
  </tr>`).join('');"""

new_rows = """  const rows = sortedP.map((p,i)=>{
    const flParts=(p.flightNumber||'').split('/').map(s=>s.trim());
    const arrFl=flParts[0]||'—';
    const retFl=flParts[1]||'—';
    return `<tr>
    <td style="text-align:center">${i+1}</td>
    <td><b>${isAr?p.arabicName:(p.englishName||p.arabicName)}</b></td>
    <td>${p.nationality||'—'}</td>
    <td dir="ltr">${p.phone||'—'}</td>
    <td><code>${p.passportNumber||'—'}</code></td>
    <td>${p.departureDateTrip||'—'}</td>
    <td>${p.departureTimeTrip||'—'}</td>
    <td dir="ltr" style="font-size:11px"><code style="background:#e0f2fe;padding:2px 6px;border-radius:4px;color:#0369a1">${arrFl}</code></td>
    <td>${p.returnDateTrip||'—'}</td>
    <td>${p.returnTimeTrip||'—'}</td>
    <td dir="ltr" style="font-size:11px"><code style="background:#fef9c3;padding:2px 6px;border-radius:4px;color:#854d0e">${retFl}</code></td>
  </tr>`;}).join('');"""

if old_rows not in content:
    print('ERROR: flights rows block not found')
    exit(1)

content = content.replace(old_rows, new_rows, 1)

# Update the L object to add new column headers
old_L = """  const L = isAr
    ? {title:'مواعيد الوصول والمغادرة',name:'الاسم',nat:'الجنسية',phone:'الهاتف',pass:'رقم الجواز',dep:'يوم الوصول',depT:'وقت الوصول',ret:'يوم المغادرة',retT:'وقت المغادرة',footer:'Raad Dojo · معسكر تايلاند 2025'}
    : {title:'Arrival & Departure Schedule',name:'Name',nat:'Nationality',phone:'Phone',pass:'Passport No.',dep:'Arrival Date',depT:'Arr. Time',ret:'Departure Date',retT:'Dep. Time',footer:'Raad Dojo · Thailand Camp 2025'};"""

new_L = """  const L = isAr
    ? {title:'مواعيد الوصول والمغادرة',name:'الاسم',nat:'الجنسية',phone:'الهاتف',pass:'رقم الجواز',dep:'يوم الوصول',depT:'وقت الوصول',arrFl:'رحلة الوصول (HKT)',ret:'يوم المغادرة',retT:'وقت المغادرة',retFl:'رحلة المغادرة (HKT)',footer:'Raad Dojo · معسكر تايلاند 2025'}
    : {title:'Arrival & Departure Schedule',name:'Name',nat:'Nationality',phone:'Phone',pass:'Passport No.',dep:'Arrival Date',depT:'Arr. Time',arrFl:'Arr. Flight (HKT)',ret:'Departure Date',retT:'Dep. Time',retFl:'Dep. Flight (HKT)',footer:'Raad Dojo · Thailand Camp 2025'};"""

if old_L not in content:
    print('ERROR: L object not found')
    exit(1)

content = content.replace(old_L, new_L, 1)

# Update the table headers to include the new columns
old_headers = """      <thead><tr>
        <th>#</th><th>${L.name}</th><th>${L.nat}</th><th>${L.phone}</th><th>${L.pass}</th>
        <th>${L.dep}</th><th>${L.depT}</th><th>${L.ret}</th><th>${L.retT}</th>
      </tr></thead>"""

new_headers = """      <thead><tr>
        <th>#</th><th>${L.name}</th><th>${L.nat}</th><th>${L.phone}</th><th>${L.pass}</th>
        <th>${L.dep}</th><th>${L.depT}</th><th>${L.arrFl}</th><th>${L.ret}</th><th>${L.retT}</th><th>${L.retFl}</th>
      </tr></thead>"""

if old_headers not in content:
    print('ERROR: table headers not found')
    exit(1)

content = content.replace(old_headers, new_headers, 1)

print('_buildFlightsReport fix done')

# ============================================================
# 3. Bump DATA_VERSION to v13
# ============================================================
content = content.replace("const DATA_VERSION = '20260610-v12';", "const DATA_VERSION = '20260612-v13';")
print('DATA_VERSION bumped to v13')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Saved. Size:', len(content))
