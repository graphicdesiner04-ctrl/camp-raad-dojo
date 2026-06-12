import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'G:\claude\Website el Waleed\camp-dashboard.html'
with open(path, encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 1. Add Turki Al-Khalidi as participant id:11 with isGuestOnly
#    Same dates/hotel/airline as Mishari (id:10)
# ============================================================
old_ps_end = '];  // end DEFAULT_PARTICIPANTS'
if old_ps_end not in content:
    # try alternate
    old_ps_end = '];\n'
    # Find the closing bracket of DEFAULT_PARTICIPANTS array
    idx = content.find('"files":[]}]\n;')
    if idx == -1:
        idx = content.find('"files":[]}]\n')
    print('Using fallback search for array end')

turki_entry = ',\n  {id:11,campId:1,arabicName:"تركي الخالدي",englishName:"TURKI ALKHALIDI",nationality:"Saudi Arabia",countryCode:"SAU",passportNumber:"",phone:"",hotel:"The Blue Mavi",roomType:"Single",roomOccupants:"1",checkIn:"2026-06-17",checkOut:"2026-06-30",airline:"Etihad Airways",flightNumber:"EY572 / EY410",departureDateTrip:"2026-06-17",departureTimeTrip:"06:40",returnDateTrip:"2026-06-30",returnTimeTrip:"",totalAmount:"0",firstPayment:"0",secondPayment:"",paymentStatus:"",registrationStatus:"ضيف",isGuestOnly:true,notes:"ضيف — يظهر في جدول الرحلات وخطاب الفندق فقط",files:[]}'

# Find end of participants array (last participant entry before ];)
old_last_p_end = '"files":[]}]\n'
new_last_p_end = '"files":[]}' + turki_entry + ']\n'

if old_last_p_end not in content:
    print('ERROR: participants array end not found')
    exit(1)

content = content.replace(old_last_p_end, new_last_p_end, 1)
print('Turki added to DEFAULT_PARTICIPANTS')

# ============================================================
# 2. Exclude isGuestOnly from all reports EXCEPT flights schedule & hotel letters
# ============================================================

# Helper: Add &&!p.isGuestOnly to participant filter expressions
# Pattern: !p.isCancelled&&!p.isUnconfirmed&&p.campId===currentCampId
# We add &&!p.isGuestOnly after isUnconfirmed check

# These are the functions that should EXCLUDE isGuestOnly:
# _buildParticipantsReport, _buildTshirtsReport, _buildPaymentsReport,
# _buildHotelReport, _buildReceipts, _buildRemainingInvoices
# renderParticipants, renderHotel, renderFlights (bianaat table), renderPayments

# The functions that should INCLUDE isGuestOnly (no change):
# _buildFlightsReport, _buildHotelLetters, renderFlightsSchedule

# Strategy: Replace the specific filter lines in each function

replacements = [
    # _buildParticipantsReport
    (
        'participants.filter(p=>!p.isCancelled&&!p.isUnconfirmed&&p.campId===currentCampId).map((p,i)=>`<tr>\n    <td style="text-align:center">${i+1}</td>\n    <td><b>${isAr?p.arabicName:(p.englishName||p.arabicName)}</b></td>\n    <td>${p.nationality||\'—\'}</td>\n    <td dir="ltr">${p.phone||\'—\'}</td>\n    <td>${p.passportNumber',
        'participants.filter(p=>!p.isCancelled&&!p.isUnconfirmed&&!p.isGuestOnly&&p.campId===currentCampId).map((p,i)=>`<tr>\n    <td style="text-align:center">${i+1}</td>\n    <td><b>${isAr?p.arabicName:(p.englishName||p.arabicName)}</b></td>\n    <td>${p.nationality||\'—\'}</td>\n    <td dir="ltr">${p.phone||\'—\'}</td>\n    <td>${p.passportNumber'
    ),
    # _buildTshirtsReport
    (
        'const activePs = participants.filter(p=>!p.isCancelled&&!p.isUnconfirmed&&p.campId===currentCampId);',
        'const activePs = participants.filter(p=>!p.isCancelled&&!p.isUnconfirmed&&!p.isGuestOnly&&p.campId===currentCampId);'
    ),
    # _buildPaymentsReport
    (
        'participants.filter(p=>!p.isCancelled&&!p.isUnconfirmed&&p.campId===currentCampId).map((p,i)=>`<tr>\n    <td style="text-align:center">${i+1}</td>\n    <td><b>${isAr?p.arabicName:(p.englishName||p.arabicName)}</b></td>\n    <td>${p.nationality||\'—\'}</td>\n    <td dir="ltr">${p.phone||\'—\'}</td>\n    <td>${p.paymentMethod',
        'participants.filter(p=>!p.isCancelled&&!p.isUnconfirmed&&!p.isGuestOnly&&p.campId===currentCampId).map((p,i)=>`<tr>\n    <td style="text-align:center">${i+1}</td>\n    <td><b>${isAr?p.arabicName:(p.englishName||p.arabicName)}</b></td>\n    <td>${p.nationality||\'—\'}</td>\n    <td dir="ltr">${p.phone||\'—\'}</td>\n    <td>${p.paymentMethod'
    ),
    # _buildHotelReport
    (
        'const rows = participants.filter(p=>!p.isCancelled&&!p.isUnconfirmed&&p.campId===currentCampId).map((p,i)=>`<tr>\n    <td style="text-align:center">${i+1}</td>\n    <td><b>${isAr?p.arabicName:(p.englishName||p.arabicName)}</b></td>\n    <td>${p.nationality||\'—\'}</td>\n    <td dir="ltr">${p.phone||\'—\'}</td>\n    <td>${p.checkIn',
        'const rows = participants.filter(p=>!p.isCancelled&&!p.isUnconfirmed&&!p.isGuestOnly&&p.campId===currentCampId).map((p,i)=>`<tr>\n    <td style="text-align:center">${i+1}</td>\n    <td><b>${isAr?p.arabicName:(p.englishName||p.arabicName)}</b></td>\n    <td>${p.nationality||\'—\'}</td>\n    <td dir="ltr">${p.phone||\'—\'}</td>\n    <td>${p.checkIn'
    ),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new, 1)
        print(f'Filter updated: ...{old[:60].strip()}...')
    else:
        print(f'WARNING not found: ...{old[:60].strip()}...')

# renderParticipants, renderHotel, renderFlights, renderPayments use campPs pattern
# Replace these carefully - they use campPs filter
# renderParticipants
content = content.replace(
    'const campPs = participants.filter(p=>p.campId===currentCampId&&!p.isCancelled&&!p.isUnconfirmed);\n  campPs.sort',
    'const campPs = participants.filter(p=>p.campId===currentCampId&&!p.isCancelled&&!p.isUnconfirmed&&!p.isGuestOnly);\n  campPs.sort',
    1
)

# renderHotel
content = content.replace(
    'const campPs = participants.filter(p=>p.campId===currentCampId&&!p.isCancelled&&!p.isUnconfirmed);\n  const assigned',
    'const campPs = participants.filter(p=>p.campId===currentCampId&&!p.isCancelled&&!p.isUnconfirmed&&!p.isGuestOnly);\n  const assigned',
    1
)

# renderFlights (bianaat al-tayaran table)
content = content.replace(
    'const campPs = participants.filter(p=>p.campId===currentCampId&&!p.isCancelled&&!p.isUnconfirmed);\n  const set',
    'const campPs = participants.filter(p=>p.campId===currentCampId&&!p.isCancelled&&!p.isUnconfirmed&&!p.isGuestOnly);\n  const set',
    1
)

# renderPayments
content = content.replace(
    'const campPs = participants.filter(p=>p.campId===currentCampId&&!p.isCancelled&&!p.isUnconfirmed);\n  const totalPaid',
    'const campPs = participants.filter(p=>p.campId===currentCampId&&!p.isCancelled&&!p.isUnconfirmed&&!p.isGuestOnly);\n  const totalPaid',
    1
)

# renderReports stats
content = content.replace(
    'const activePs = participants.filter(p=>!p.isCancelled&&!p.isUnconfirmed);\n  const totalPaid',
    'const activePs = participants.filter(p=>!p.isCancelled&&!p.isUnconfirmed&&!p.isGuestOnly);\n  const totalPaid',
    1
)

# receipts and remaining invoices
content = content.replace(
    'participants.filter(p=>!p.isCancelled&&!p.isUnconfirmed&&p.campId===currentCampId).forEach',
    'participants.filter(p=>!p.isCancelled&&!p.isUnconfirmed&&!p.isGuestOnly&&p.campId===currentCampId).forEach',
    1
)

print('Dashboard/report filters updated')

# ============================================================
# 3. Fix 2025 → 2026 everywhere in reports and hotel letter
# ============================================================
replacements_2025 = [
    ('معسكر تايلاند 2025', 'معسكر تايلاند 2026'),
    ('Thailand Camp 2025', 'Thailand Camp 2026'),
    ('Camp Thailand 2025', 'Camp Thailand 2026'),
    ('CAMP THAILAND – RAAD DOJO 2025', 'CAMP THAILAND – RAAD DOJO 2026'),
    ('معسكر تايلاند 2025', 'معسكر تايلاند 2026'),
]

for old, new in replacements_2025:
    count = content.count(old)
    content = content.replace(old, new)
    print(f'2025→2026: "{old}" replaced {count}x')

# ============================================================
# 4. Bump DATA_VERSION to v16
# ============================================================
content = content.replace("const DATA_VERSION = '20260612-v15';", "const DATA_VERSION = '20260612-v16';")
print('DATA_VERSION → v16')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Saved. Size:', len(content))
