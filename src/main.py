from src.storage.data_handler import DataHandler
from src.services.tracker_service import TrackerService
from src.services.report_service import ReportService
from src.utils.validators import *

def show(rows):
    if not rows: print("\nNo records found."); return
    print(f"\n{'ID':<5}{'Date':<13}{'Category':<16}{'Amount':>12}{'Payment':<16}Description")
    print("-"*105)
    for r in rows: print(f"{r['expense_id']:<5}{r['expense_date']:<13}{r['category']:<16}{r['amount']:>12.2f}{r['payment_mode']:<16}{r['description']}")
def expense_input(i=None):
    d=parse_date(input("Date (YYYY-MM-DD): ")); c=valid_category(input("Category: ")); a=positive_amount(input("Amount: ")); m=valid_payment_mode(input("Payment mode: ")); desc=input("Description: ").strip()
    if not desc: raise ValueError("Description cannot be empty.")
    return i,d,c,a,m,desc
def main():
    store=DataHandler(); tracker=TrackerService(store); reports=ReportService(store)
    while True:
        print("\n=== SMART EXPENSE TRACKER ===\n1 Add Expense\n2 Update Expense\n3 Delete Expense\n4 View/Filter\n5 Search\n6 Set Budget\n7 Budget Status\n8 Monthly Report\n9 Export CSV/PDF\n10 Visualizations\n11 Backup/Restore\n0 Exit")
        ch=input("Choose: ").strip()
        try:
            if ch=="1":
                _,d,c,a,m,x=expense_input(); print("Added ID:",tracker.add_expense(d,c,a,m,x))
            elif ch=="2":
                i=int(input("Expense ID: ")); _,d,c,a,m,x=expense_input(i); tracker.update_expense(i,d,c,a,m,x); print("Updated.")
            elif ch=="3":
                i=int(input("Expense ID: ")); print("Deleted." if tracker.delete_expense(i) else "ID not found.")
            elif ch=="4":
                s=input("Start date (blank=any): "); e=input("End date (blank=any): "); c=input("Category (blank=any): "); m=input("Payment mode (blank=any): ")
                show(store.get_expenses(parse_date(s) if s else None,parse_date(e) if e else None,valid_category(c) if c else None,valid_payment_mode(m) if m else None))
            elif ch=="5": show(store.search_expenses(input("Keyword: ")))
            elif ch=="6":
                mo=valid_month(input("Month YYYY-MM: ")); tracker.set_budget(mo,valid_category(input("Category: ")),positive_amount(input("Budget limit: "))); print("Budget saved.")
            elif ch=="7":
                for r in tracker.budget_status(valid_month(input("Month YYYY-MM: "))): print(f"{r['category']:<16} Budget Rs.{r['limit_amount']:<10.2f} Actual Rs.{r['actual']:<10.2f} {r['percent']:>6.1f}% {r['alert']}")
            elif ch=="8":
                s=reports.monthly_summary(valid_month(input("Month YYYY-MM: "))); print(f"Total: Rs.{s['total']:.2f}\nAverage daily: Rs.{s['average_daily']:.2f}\nHighest category: {s['highest_category']}"); print(s["category_summary"].to_string(index=False) if not s["category_summary"].empty else "No expenses.")
            elif ch=="9":
                mo=valid_month(input("Month YYYY-MM: ")); print("CSV:",reports.export_csv(mo)); print("PDF:",reports.export_pdf(mo))
            elif ch=="10":
                mo=valid_month(input("Month YYYY-MM: ")); print("Pie:",reports.plot_pie(mo)); print("Trend:",reports.plot_trend(mo)); print("Budget:",reports.plot_budget_vs_actual(mo))
            elif ch=="11":
                a=input("backup or restore: ").lower().strip(); p=input("Path [data/backup.json]: ").strip() or "data/backup.json"
                store.backup(p) if a=="backup" else store.restore(p) if a=="restore" else (_ for _ in ()).throw(ValueError("Choose backup or restore."))
                print("Operation completed.")
            elif ch=="0": print("Goodbye!"); break
            else: print("Invalid option.")
        except (ValueError,OSError,KeyError) as e: print("Error:",e)
        except Exception as e: print("Unexpected error:",e)
if __name__=="__main__": main()
