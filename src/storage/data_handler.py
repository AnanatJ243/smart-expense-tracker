from pathlib import Path
import json, sqlite3

class DataHandler:
    def __init__(self, db_path="data/expenses.db"):
        self.db_path=Path(db_path); self.db_path.parent.mkdir(parents=True, exist_ok=True); self._initialize()
    def connect(self):
        con=sqlite3.connect(self.db_path); con.row_factory=sqlite3.Row; return con
    def _initialize(self):
        with self.connect() as con:
            con.executescript("""CREATE TABLE IF NOT EXISTS expenses(
            expense_id INTEGER PRIMARY KEY AUTOINCREMENT, expense_date TEXT NOT NULL,
            category TEXT NOT NULL, amount REAL NOT NULL CHECK(amount>0),
            payment_mode TEXT NOT NULL, description TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS budgets(
            budget_id INTEGER PRIMARY KEY AUTOINCREMENT, month TEXT NOT NULL,
            category TEXT NOT NULL, limit_amount REAL NOT NULL CHECK(limit_amount>0),
            UNIQUE(month,category));""")
    def add_expense(self,e):
        with self.connect() as con:
            return con.execute("INSERT INTO expenses(expense_date,category,amount,payment_mode,description) VALUES(?,?,?,?,?)",e.to_tuple()).lastrowid
    def update_expense(self,e):
        with self.connect() as con:
            con.execute("UPDATE expenses SET expense_date=?,category=?,amount=?,payment_mode=?,description=? WHERE expense_id=?",(*e.to_tuple(),e.expense_id))
    def delete_expense(self,i):
        with self.connect() as con: return con.execute("DELETE FROM expenses WHERE expense_id=?",(i,)).rowcount
    def get_expenses(self,start=None,end=None,category=None,payment_mode=None):
        q="SELECT * FROM expenses WHERE 1=1"; p=[]
        if start: q+=" AND expense_date>=?"; p.append(start)
        if end: q+=" AND expense_date<=?"; p.append(end)
        if category: q+=" AND category=?"; p.append(category)
        if payment_mode: q+=" AND payment_mode=?"; p.append(payment_mode)
        q+=" ORDER BY expense_date DESC,expense_id DESC"
        with self.connect() as con: return [dict(r) for r in con.execute(q,p).fetchall()]
    def search_expenses(self,k):
        with self.connect() as con: return [dict(r) for r in con.execute("SELECT * FROM expenses WHERE description LIKE ? ORDER BY expense_date DESC",(f"%{k}%",)).fetchall()]
    def set_budget(self,month,category,limit_amount):
        with self.connect() as con: con.execute("INSERT INTO budgets(month,category,limit_amount) VALUES(?,?,?) ON CONFLICT(month,category) DO UPDATE SET limit_amount=excluded.limit_amount",(month,category,limit_amount))
    def get_budgets(self,month=None):
        q="SELECT * FROM budgets"; p=[]
        if month: q+=" WHERE month=?"; p.append(month)
        q+=" ORDER BY month DESC,category"
        with self.connect() as con: return [dict(r) for r in con.execute(q,p).fetchall()]
    def backup(self,path):
        Path(path).parent.mkdir(parents=True,exist_ok=True)
        Path(path).write_text(json.dumps({"expenses":self.get_expenses(),"budgets":self.get_budgets()},indent=2),encoding="utf-8")
    def restore(self,path):
        data=json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(data,dict) or not isinstance(data.get("expenses"),list) or not isinstance(data.get("budgets"),list): raise ValueError("Invalid backup format.")
        with self.connect() as con:
            con.execute("DELETE FROM expenses"); con.execute("DELETE FROM budgets")
            for e in data["expenses"]: con.execute("INSERT INTO expenses VALUES(?,?,?,?,?,?)",(e["expense_id"],e["expense_date"],e["category"],e["amount"],e["payment_mode"],e["description"]))
            for b in data["budgets"]: con.execute("INSERT INTO budgets VALUES(?,?,?,?)",(b["budget_id"],b["month"],b["category"],b["limit_amount"]))
