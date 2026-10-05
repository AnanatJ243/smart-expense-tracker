from src.models.expense import Expense

class TrackerService:
    def __init__(self,storage): self.storage=storage
    def add_expense(self,d,c,a,m,desc): return self.storage.add_expense(Expense(None,d,c,a,m,desc))
    def update_expense(self,i,d,c,a,m,desc): self.storage.update_expense(Expense(i,d,c,a,m,desc))
    def delete_expense(self,i): return self.storage.delete_expense(i)
    def set_budget(self,month,category,amount): self.storage.set_budget(month,category,amount)
    def budget_status(self,month):
        spent={}
        for e in self.storage.get_expenses(f"{month}-01",f"{month}-31"): spent[e["category"]]=spent.get(e["category"],0)+e["amount"]
        out=[]
        for b in self.storage.get_budgets(month):
            actual=spent.get(b["category"],0); pct=actual/b["limit_amount"]*100
            out.append({**b,"actual":round(actual,2),"percent":round(pct,1),"alert":"OVER 100%" if pct>=100 else "OVER 80%" if pct>=80 else "OK"})
        return out
