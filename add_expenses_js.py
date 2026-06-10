import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'G:\claude\Website el Waleed\camp-dashboard.html'
with open(path, encoding='utf-8') as f:
    content = f.read()

expenses_js = r"""
// ========== EXPENSES ==========
const EXPENSE_CATEGORIES = ['إقامة','طعام وشراب','نقل','تدريب ومعدات','ترفيه وجولات','رسوم إدارية','أخرى'];

function getExpenses(){ return load('camp_expenses_'+currentCampId, []); }
function saveExpenses(arr){ save('camp_expenses_'+currentCampId, arr); }
function getThbRate(){ return parseFloat(localStorage.getItem('thb_rate')||'35'); }
function saveThbRate(){
  const v = parseFloat(document.getElementById('thb-rate')?.value||35);
  if(!isNaN(v) && v>0){ localStorage.setItem('thb_rate', String(v)); renderExpenses(); }
}

function renderExpenses(){
  const expenses = getExpenses();
  const rate = getThbRate();
  const rateEl = document.getElementById('thb-rate');
  if(rateEl && document.activeElement!==rateEl) rateEl.value = rate;

  const totalTHB = expenses.reduce((s,e)=>s+(parseFloat(e.amountTHB)||0),0);
  const totalUSD = totalTHB / rate;

  const campPs = participants.filter(p=>p.campId===currentCampId&&!p.isCancelled&&!p.isUnconfirmed);
  const revenueUSD = campPs.reduce((s,p)=>{
    return s + (parseFloat(p.firstPayment||0)) + (parseFloat(p.secondPayment||0));
  },0);
  const profitUSD = revenueUSD - totalUSD;
  const profitTHB = profitUSD * rate;
  const isProfit = profitUSD >= 0;

  const summary = document.getElementById('expenses-summary');
  if(summary){
    summary.innerHTML = `
      <div class="stat-card"><div class="stat-icon green">💵</div><div>
        <div class="stat-value">$${revenueUSD.toLocaleString('en',{minimumFractionDigits:0,maximumFractionDigits:0})}</div>
        <div class="stat-label">إجمالي الإيرادات (USD)</div>
      </div></div>
      <div class="stat-card"><div class="stat-icon red">🧾</div><div>
        <div class="stat-value">${Math.round(totalTHB).toLocaleString('en')} ฿</div>
        <div class="stat-label">إجمالي المصروفات (THB)</div>
      </div></div>
      <div class="stat-card"><div class="stat-icon red">💸</div><div>
        <div class="stat-value">$${totalUSD.toLocaleString('en',{minimumFractionDigits:0,maximumFractionDigits:0})}</div>
        <div class="stat-label">إجمالي المصروفات (USD)</div>
      </div></div>
      <div class="stat-card" style="border:2px solid ${isProfit?'var(--success)':'var(--danger)'}">
        <div class="stat-icon" style="background:${isProfit?'#dcfce7':'#fee2e2'}">${isProfit?'📈':'📉'}</div>
        <div>
          <div class="stat-value" style="color:${isProfit?'var(--success)':'var(--danger)'}">
            ${isProfit?'+':''}${profitUSD.toLocaleString('en',{minimumFractionDigits:0,maximumFractionDigits:0})} $
          </div>
          <div class="stat-label">${isProfit?'✅ صافي الربح':'❌ خسارة'} (USD)</div>
        </div>
      </div>
    `;
  }

  const tbody = document.getElementById('expenses-tbody');
  if(!tbody) return;
  if(!expenses.length){
    tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;padding:32px;color:var(--muted)">لا توجد مصروفات بعد — اضغط + إضافة مصروف</td></tr>';
  } else {
    tbody.innerHTML = expenses.map((e,i)=>{
      const usd = (parseFloat(e.amountTHB)||0)/rate;
      return `<tr style="border-bottom:1px solid var(--border)">
        <td style="text-align:center;padding:10px 12px;color:var(--muted)">${i+1}</td>
        <td style="padding:10px 12px;font-weight:500">${e.desc}</td>
        <td style="padding:10px 12px;text-align:center">
          <span style="background:#f1f5f9;border-radius:20px;padding:3px 10px;font-size:12px">${e.category||'أخرى'}</span>
        </td>
        <td style="padding:10px 12px;text-align:left;font-weight:600">${parseFloat(e.amountTHB||0).toLocaleString('en')} ฿</td>
        <td style="padding:10px 12px;text-align:left;color:var(--danger)">$${usd.toLocaleString('en',{minimumFractionDigits:2,maximumFractionDigits:2})}</td>
        <td style="padding:10px 12px;text-align:center">
          <button class="btn btn-edit" style="font-size:11px;padding:4px 8px" onclick="editExpense(${e.id})">✏️ تعديل</button>
          <button class="btn btn-danger" style="font-size:11px;padding:4px 8px;margin-right:4px" onclick="deleteExpense(${e.id})">🗑️</button>
        </td>
      </tr>`;
    }).join('');
  }

  const tfoot = document.getElementById('expenses-tfoot');
  if(tfoot && expenses.length){
    tfoot.innerHTML = `
      <tr style="background:#f8fafc;font-weight:700;border-top:2px solid var(--border)">
        <td colspan="3" style="padding:12px;text-align:right">الإجمالي</td>
        <td style="padding:12px;text-align:left;font-size:15px">${Math.round(totalTHB).toLocaleString('en')} ฿</td>
        <td style="padding:12px;text-align:left;font-size:15px;color:var(--danger)">$${totalUSD.toLocaleString('en',{minimumFractionDigits:2,maximumFractionDigits:2})}</td>
        <td></td>
      </tr>
      <tr style="background:${isProfit?'#dcfce7':'#fee2e2'};font-weight:700">
        <td colspan="3" style="padding:12px;text-align:right;color:${isProfit?'var(--success)':'var(--danger)'}">
          ${isProfit?'✅ صافي الربح':'❌ الخسارة'}
        </td>
        <td style="padding:12px;text-align:left;color:${isProfit?'var(--success)':'var(--danger)'}">
          ${isProfit?'+':'-'}${Math.round(Math.abs(profitTHB)).toLocaleString('en')} ฿
        </td>
        <td style="padding:12px;text-align:left;color:${isProfit?'var(--success)':'var(--danger)'}">
          ${isProfit?'+':'-'}$${Math.abs(profitUSD).toLocaleString('en',{minimumFractionDigits:2,maximumFractionDigits:2})}
        </td>
        <td></td>
      </tr>
    `;
  } else if(tfoot){
    tfoot.innerHTML='';
  }
}

let editingExpenseId = null;

function openExpenseModal(id){
  editingExpenseId = id||null;
  const expenses = getExpenses();
  const e = id ? expenses.find(x=>x.id===id) : null;
  const cats = EXPENSE_CATEGORIES.map(c=>`<option value="${c}" ${e&&e.category===c?'selected':''}>${c}</option>`).join('');
  const html = `
    <div id="modal-expense" style="display:flex;position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:9999;align-items:center;justify-content:center" onclick="if(event.target===this)this.remove()">
      <div style="background:#fff;border-radius:16px;padding:28px;max-width:440px;width:92%;box-shadow:0 20px 60px rgba(0,0,0,.25)">
        <h3 style="margin:0 0 20px;font-size:18px">${id?'✏️ تعديل مصروف':'➕ إضافة مصروف جديد'}</h3>
        <div style="display:flex;flex-direction:column;gap:14px">
          <label style="font-size:13px;font-weight:600;display:block">الوصف
            <input id="exp-desc" type="text" value="${e?e.desc:''}" placeholder="مثال: فندق ليلة 15 يونيو"
              style="display:block;width:100%;box-sizing:border-box;margin-top:6px;padding:9px 12px;border:1px solid var(--border);border-radius:8px;font-size:14px;font-family:inherit">
          </label>
          <label style="font-size:13px;font-weight:600;display:block">الفئة
            <select id="exp-cat" style="display:block;width:100%;box-sizing:border-box;margin-top:6px;padding:9px 12px;border:1px solid var(--border);border-radius:8px;font-size:14px;font-family:inherit">
              ${cats}
            </select>
          </label>
          <label style="font-size:13px;font-weight:600;display:block">المبلغ بالبات (THB) ฿
            <input id="exp-thb" type="number" value="${e?e.amountTHB:''}" min="0" step="1" placeholder="0"
              style="display:block;width:100%;box-sizing:border-box;margin-top:6px;padding:9px 12px;border:1px solid var(--border);border-radius:8px;font-size:14px;font-family:inherit">
          </label>
        </div>
        <div style="display:flex;gap:10px;margin-top:22px;justify-content:flex-end">
          <button onclick="document.getElementById('modal-expense').remove()"
            style="padding:9px 22px;border:1px solid var(--border);border-radius:8px;background:#fff;cursor:pointer;font-family:inherit;font-size:14px">إلغاء</button>
          <button onclick="saveExpense()"
            style="padding:9px 22px;background:var(--primary);color:#fff;border:none;border-radius:8px;cursor:pointer;font-family:inherit;font-size:14px;font-weight:600">حفظ</button>
        </div>
      </div>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', html);
  setTimeout(()=>document.getElementById('exp-desc')?.focus(), 80);
}

function saveExpense(){
  const desc = (document.getElementById('exp-desc')?.value||'').trim();
  const cat  = document.getElementById('exp-cat')?.value || 'أخرى';
  const thb  = parseFloat(document.getElementById('exp-thb')?.value)||0;
  if(!desc){ alert('أدخل وصف المصروف'); return; }
  if(!thb || thb<=0){ alert('أدخل المبلغ بالبات'); return; }
  const expenses = getExpenses();
  if(editingExpenseId){
    const idx = expenses.findIndex(e=>e.id===editingExpenseId);
    if(idx>=0){ expenses[idx].desc=desc; expenses[idx].category=cat; expenses[idx].amountTHB=thb; }
  } else {
    const newId = expenses.length ? Math.max(...expenses.map(e=>e.id))+1 : 1;
    expenses.push({id:newId, desc, category:cat, amountTHB:thb});
  }
  saveExpenses(expenses);
  document.getElementById('modal-expense')?.remove();
  renderExpenses();
  toast(editingExpenseId?'تم تعديل المصروف ✅':'تمت إضافة المصروف ✅','success');
}

function editExpense(id){ openExpenseModal(id); }

function deleteExpense(id){
  if(!confirm('حذف هذا المصروف؟')) return;
  saveExpenses(getExpenses().filter(e=>e.id!==id));
  renderExpenses();
  toast('تم حذف المصروف','success');
}
"""

old_final = '// ===== FINAL INIT'
if old_final not in content:
    print('ERROR: anchor not found')
    exit(1)

content = content.replace(old_final, expenses_js + '\n' + old_final, 1)

print('renderExpenses in content:', 'renderExpenses' in content)
print('openExpenseModal in content:', 'openExpenseModal' in content)
print('saveExpense in content:', 'saveExpense' in content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Saved. Size:', len(content))
