import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'G:\claude\Website el Waleed\camp-dashboard.html'
with open(path, encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 1. Add schedule card HTML to page-flights
# ============================================================
old_flights_page_end = '''  </div>
</div>

<!-- ======== PAGE: FILES ======== -->'''

new_flights_page_end = '''  </div>

  <div class="card" style="margin-top:20px">
    <div class="card-header">
      <div class="card-title">📅 جدول مواعيد الوصول والمغادرة من بوكيت</div>
    </div>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>#</th><th>الاسم</th>
            <th>📅 يوم الوصول (HKT)</th><th>🕐 وقت الوصول</th><th>✈️ رحلة الوصول</th>
            <th>📅 يوم المغادرة (HKT)</th><th>🕐 وقت المغادرة</th><th>✈️ رحلة المغادرة</th>
          </tr>
        </thead>
        <tbody id="flights-schedule-tbody"></tbody>
      </table>
    </div>
  </div>
</div>

<!-- ======== PAGE: FILES ======== -->'''

if old_flights_page_end not in content:
    print('ERROR: flights page end not found')
    exit(1)

content = content.replace(old_flights_page_end, new_flights_page_end, 1)
print('flights schedule card HTML added')

# ============================================================
# 2. Add renderFlightsSchedule() function and call it from renderFlights()
# ============================================================
old_render_flights_end = '''  }).join('');
}

// ========== FILES =========='''

new_render_flights_end = '''  }).join('');
  renderFlightsSchedule();
}

function renderFlightsSchedule(){
  const campPs = participants.filter(p=>p.campId===currentCampId&&!p.isCancelled&&!p.isUnconfirmed);
  const sorted = campPs.slice().sort((a,b)=>{
    const da=(a.departureDateTrip||'9999')+' '+(a.departureTimeTrip||'00:00');
    const db=(b.departureDateTrip||'9999')+' '+(b.departureTimeTrip||'00:00');
    return da.localeCompare(db);
  });
  const tbody = document.getElementById('flights-schedule-tbody');
  if(!tbody) return;
  tbody.innerHTML = sorted.map((p,i)=>{
    const parts=(p.flightNumber||'').split('/').map(s=>s.trim());
    const arrFl=parts[0]||'—';
    const retFl=parts[1]||'—';
    const noData='<span style="color:#cbd5e1">—</span>';
    const flStyle='background:#f1f5f9;padding:2px 8px;border-radius:4px;font-size:12px;font-family:monospace';
    const arrFlStyle='background:#e0f2fe;padding:2px 8px;border-radius:4px;font-size:12px;font-family:monospace;color:#0369a1';
    const retFlStyle='background:#fef9c3;padding:2px 8px;border-radius:4px;font-size:12px;font-family:monospace;color:#854d0e';
    return `<tr>
      <td style="text-align:center">${i+1}</td>
      <td><div class="name-cell"><span class="name-ar">${p.arabicName}</span></div></td>
      <td>${p.departureDateTrip||noData}</td>
      <td style="font-weight:600">${p.departureTimeTrip||noData}</td>
      <td dir="ltr">${p.flightNumber?`<code style="${arrFlStyle}">${arrFl}</code>`:noData}</td>
      <td>${p.returnDateTrip||noData}</td>
      <td style="font-weight:600">${p.returnTimeTrip||noData}</td>
      <td dir="ltr">${p.flightNumber&&retFl&&retFl!==arrFl?`<code style="${retFlStyle}">${retFl}</code>`:noData}</td>
    </tr>`;
  }).join('');
}

// ========== FILES =========='''

if old_render_flights_end not in content:
    print('ERROR: renderFlights end not found')
    exit(1)

content = content.replace(old_render_flights_end, new_render_flights_end, 1)
print('renderFlightsSchedule() function added')

# ============================================================
# 3. Bump DATA_VERSION to v14 (force cache clear for all users)
# ============================================================
content = content.replace("const DATA_VERSION = '20260612-v13';", "const DATA_VERSION = '20260612-v14';")
print('DATA_VERSION bumped to v14')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Saved. Size:', len(content))
