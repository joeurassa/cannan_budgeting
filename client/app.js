const STORAGE_KEY = "budget_transactions_v1";

const els = {
  form: document.getElementById("txForm"),
  type: document.getElementById("type"),
  amount: document.getElementById("amount"),
  category: document.getElementById("category"),
  description: document.getElementById("description"),
  error: document.getElementById("formError"),
  txBody: document.getElementById("txBody"),
  incomeTotal: document.getElementById("incomeTotal"),
  expenseTotal: document.getElementById("expenseTotal"),
  balanceTotal: document.getElementById("balanceTotal"),
  clearAll: document.getElementById("clearAll"),
};

function loadTransactions() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function saveTransactions(list) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
}

function formatMoneyFromCents(cents) {
  const sign = cents < 0 ? "-" : "";
  const abs = Math.abs(cents);
  const dollars = Math.floor(abs / 100);
  const rem = abs % 100;
  return `${sign}$${dollars.toLocaleString()}.${String(rem).padStart(2, "0")}`;
}

/**
 * Parse a money string like "12.34" into integer cents.
 * Rules:
 * - non-negative only
 * - up to 2 decimals
 * - rejects commas/spaces
 */
function parseMoneyToCents(input) {
  const s = String(input).trim();

  // Allow "12", "12.3", "12.34" but not negatives, not commas.
  const m = s.match(/^(\d+)(?:\.(\d{1,2}))?$/);
  if (!m) return { ok: false, message: "Amount must be a valid number (max 2 decimals)." };

  const dollars = Number(m[1]);
  const centsPart = m[2] ? m[2].padEnd(2, "0") : "00";
  const cents = Number(centsPart);

  // Prevent absurdly large numbers if you want (optional)
  if (!Number.isFinite(dollars) || !Number.isFinite(cents)) {
    return { ok: false, message: "Amount is invalid." };
  }

  return { ok: true, cents: dollars * 100 + cents, normalized: `${dollars}.${centsPart}` };
}

function validateForm({ transaction_type, amountStr, category, description }) {
  const t = String(transaction_type).trim().toLowerCase();
  if (t !== "income" && t !== "expense") return { ok: false, message: "Type must be income or expense." };

  const parsed = parseMoneyToCents(amountStr);
  if (!parsed.ok) return parsed;

  if (parsed.cents < 0) return { ok: false, message: "Amount cannot be negative." };

  const cat = String(category).trim();
  if (!cat) return { ok: false, message: "Category cannot be empty." };

  const desc = String(description).trim();
  if (!desc) return { ok: false, message: "Description cannot be empty." };

  return { ok: true, transaction_type: t, amount_cents: parsed.cents, amount: parsed.normalized, category: cat, description: desc };
}

function computeTotals(list) {
  let income = 0;
  let expense = 0;

  for (const tx of list) {
    if (tx.transaction_type === "income") income += tx.amount_cents;
    else if (tx.transaction_type === "expense") expense += tx.amount_cents;
  }

  return { income, expense, balance: income - expense };
}

function render() {
  const list = loadTransactions();
  const totals = computeTotals(list);

  els.incomeTotal.textContent = formatMoneyFromCents(totals.income);
  els.expenseTotal.textContent = formatMoneyFromCents(totals.expense);
  els.balanceTotal.textContent = formatMoneyFromCents(totals.balance);

  els.txBody.innerHTML = "";

  if (list.length === 0) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td colspan="5" class="muted">No transactions yet.</td>`;
    els.txBody.appendChild(tr);
    return;
  }

  for (const tx of list) {
    const tr = document.createElement("tr");

    tr.innerHTML = `
      <td><span class="tag ${tx.transaction_type}">${tx.transaction_type}</span></td>
      <td>${formatMoneyFromCents(tx.amount_cents)}</td>
      <td>${escapeHtml(tx.category)}</td>
      <td>${escapeHtml(tx.description)}</td>
      <td><button class="btn outline danger" data-delete="${tx.id}">Delete</button></td>
    `;

    els.txBody.appendChild(tr);
  }
}

function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function addTransaction(tx) {
  const list = loadTransactions();
  list.unshift(tx); // newest first
  saveTransactions(list);
  render();
}

function deleteTransaction(id) {
  const list = loadTransactions().filter(tx => String(tx.id) !== String(id));
  saveTransactions(list);
  render();
}

function getMonthlyIncome(list) {
  const now = new Date();
  const currentMonth = now.getMonth();
  const currentYear = now.getFullYear();

  return list
    .filter(tx => {
      const d = new Date(tx.date);
      return (
        tx.transaction_type === "income" &&
        d.getMonth() === currentMonth &&
        d.getFullYear() === currentYear
      );
    })
    .reduce((sum, tx) => sum + tx.amount_cents, 0);
}



//*********************************************** */

// Form submit
els.form.addEventListener("submit", (e) => {
  e.preventDefault();
  els.error.textContent = "";

  const result = validateForm({
    transaction_type: els.type.value,
    amountStr: els.amount.value,
    category: els.category.value,
    description: els.description.value,
    date: new Date().toISOString(),
  });

  if (!result.ok) {
    els.error.textContent = result.message;
    return;
  }

  const tx = {
    id: Date.now(),
    transaction_type: result.transaction_type,
    amount: result.amount,              // string "12.34" (Python Decimal-friendly)
    amount_cents: result.amount_cents,  // integer cents (UI math)
    category: result.category,
    description: result.description,
  };

  addTransaction(tx);

  // Reset form
  els.amount.value = "";
  els.category.value = "";
  els.description.value = "";
  els.amount.focus();
});

// Delete buttons (event delegation)
els.txBody.addEventListener("click", (e) => {
  const btn = e.target.closest("button[data-delete]");
  if (!btn) return;
  deleteTransaction(btn.dataset.delete);
});

// Clear all
els.clearAll.addEventListener("click", () => {
  localStorage.removeItem(STORAGE_KEY);
  render();
});

render();