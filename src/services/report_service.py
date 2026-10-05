from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

class ReportService:
    def __init__(self,storage,reports_dir="reports"):
        self.storage=storage; self.reports_dir=Path(reports_dir); self.reports_dir.mkdir(parents=True,exist_ok=True)
    def dataframe(self,start=None,end=None,category=None,payment_mode=None): return pd.DataFrame(self.storage.get_expenses(start,end,category,payment_mode))
    def monthly_summary(self,month):
        df=self.dataframe(f"{month}-01",f"{month}-31")
        if df.empty: return {"total":0,"average_daily":0,"highest_category":"N/A","category_summary":pd.DataFrame()}
        df["expense_date"]=pd.to_datetime(df["expense_date"]); total=float(df.amount.sum()); days=df.expense_date.dt.date.nunique()
        cs=df.groupby("category",as_index=False).amount.sum().sort_values("amount",ascending=False)
        return {"total":total,"average_daily":total/max(days,1),"highest_category":cs.iloc[0].category,"category_summary":cs}
    def export_csv(self,month):
        p=self.reports_dir/f"expenses_{month}.csv"; self.dataframe(f"{month}-01",f"{month}-31").to_csv(p,index=False); return p
    def export_pdf(self,month):
        s=self.monthly_summary(month); p=self.reports_dir/f"expense_report_{month}.pdf"; c=canvas.Canvas(str(p),pagesize=A4)
        c.setFont("Helvetica-Bold",16); c.drawString(50,800,f"Expense Report - {month}"); c.setFont("Helvetica",11)
        for y,t in [(770,f"Total spending: Rs. {s['total']:.2f}"),(750,f"Average daily spending: Rs. {s['average_daily']:.2f}"),(730,f"Highest expense category: {s['highest_category']}")]: c.drawString(50,y,t)
        y=695; c.drawString(50,y,"Category"); c.drawString(250,y,"Amount"); y-=20
        for _,r in s["category_summary"].iterrows(): c.drawString(50,y,str(r.category)); c.drawString(250,y,f"Rs. {r.amount:.2f}"); y-=18
        c.save(); return p
    def plot_pie(self,month):
        df=self.dataframe(f"{month}-01",f"{month}-31")
        if df.empty: raise ValueError("No expenses found for this month.")
        plt.figure(figsize=(7,5)); df.groupby("category").amount.sum().plot.pie(autopct="%1.1f%%",ylabel=""); plt.title(f"Expense Distribution - {month}"); plt.tight_layout()
        p=self.reports_dir/f"category_pie_{month}.png"; plt.savefig(p,dpi=150); plt.close(); return p
    def plot_trend(self,month):
        df=self.dataframe(f"{month}-01",f"{month}-31")
        if df.empty: raise ValueError("No expenses found for this month.")
        df["expense_date"]=pd.to_datetime(df.expense_date); daily=df.groupby("expense_date").amount.sum()
        plt.figure(figsize=(8,5)); sns.lineplot(x=daily.index,y=daily.values,marker="o"); plt.title(f"Daily Spending Trend - {month}"); plt.xlabel("Date"); plt.ylabel("Amount"); plt.tight_layout()
        p=self.reports_dir/f"daily_trend_{month}.png"; plt.savefig(p,dpi=150); plt.close(); return p
    def plot_budget_vs_actual(self,month):
        budgets=pd.DataFrame(self.storage.get_budgets(month)); exp=pd.DataFrame(self.storage.get_expenses(f"{month}-01",f"{month}-31"))
        if budgets.empty: raise ValueError("No budgets found for this month.")
        spent=exp.groupby("category").amount.sum() if not exp.empty else pd.Series(dtype=float); budgets["actual"]=budgets.category.map(spent).fillna(0)
        plot_df=budgets.set_index("category")[["limit_amount","actual"]]
        ax=plot_df.plot(kind="bar",figsize=(9,5)); ax.set_title(f"Budget vs Actual - {month}"); ax.set_ylabel("Amount"); plt.xticks(rotation=30); plt.tight_layout()
        p=self.reports_dir/f"budget_vs_actual_{month}.png"; plt.savefig(p,dpi=150); plt.close(); return p
