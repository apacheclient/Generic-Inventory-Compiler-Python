from __future__ import annotations
import argparse
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from src.reconciler import InventoryReconciler

console = Console()

def print_summary(summary: dict) -> None:
    table = Table(title="Reconciliation Summary", box=box.ROUNDED, show_header=False)
    table.add_column("Metric", style="cyan", width=28)
    table.add_column("Value", style="bold")
    table.add_row("Total SKUs counted", str(summary["total_skus"]))
    table.add_row("Perfect matches", f"{summary['matched']}  ({summary['match_rate_pct']}%)")
    table.add_row("Shortages (shrink)", str(summary["shortages"]))
    table.add_row("Overages", str(summary["overages"]))
    table.add_row("Critical issues", f"[red]{summary['critical_count']}[/red]")
    table.add_row("High priority issues", f"[yellow]{summary['high_count']}[/yellow]")
    table.add_row("", "")
    table.add_row("Total Shrink ($)", f"[red]${summary['total_shrink_dollars']:,.2f}[/red]")
    table.add_row("Total Overage ($)", f"[green]${summary['total_overage_dollars']:,.2f}[/green]")
    table.add_row("Net Variance ($)", f"${summary['net_variance_dollars']:,.2f}")
    console.print(table)

def print_discrepancies(df, max_rows: int = 25) -> None:
    if df.empty:
        console.print("[green]No discrepancies found.[/green]")
        return
    table = Table(title=f"Top Discrepancies (showing up to {max_rows})", box=box.SIMPLE_HEAVY, show_lines=True)
    table.add_column("SKU", style="dim")
    table.add_column("Product", max_width=28)
    table.add_column("Cat", style="cyan")
    table.add_column("Sys", justify="right")
    table.add_column("Phys", justify="right")
    table.add_column("Var", justify="right")
    table.add_column("$ Impact", justify="right")
    table.add_column("Severity")
    severity_colors = {"CRITICAL": "bold red", "HIGH": "bold yellow", "MEDIUM": "yellow", "LOW": "dim"}
    for _, row in df.head(max_rows).iterrows():
        sev_style = severity_colors.get(row["severity"], "")
        table.add_row(
            row["sku"], row["product_name"], row["category"],
            str(row["system_qty"]), str(row["physical_qty"]),
            f"{row['variance_qty']:+d}", f"${row['variance_value']:+,.2f}",
            f"[{sev_style}]{row['severity']}[/{sev_style}]"
        )
    console.print(table)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--system", default="data/system_inventory.csv")
    parser.add_argument("--physical", default="data/physical_count.csv")
    parser.add_argument("--export", metavar="FILE")
    parser.add_argument("--min-severity", default="LOW", choices=["CRITICAL", "HIGH", "MEDIUM", "LOW"])
    parser.add_argument("--full-report", action="store_true")
    parser.add_argument("--max-rows", type=int, default=25)
    args = parser.parse_args()

    console.print(Panel.fit("[bold]Inventory Reconciler[/bold]\nSystem vs Physical Count", border_style="blue"))

    try:
        reconciler = InventoryReconciler(args.system, args.physical)
        reconciler.reconcile()
        summary = reconciler.summary()
        print_summary(summary)
        console.print()
        discrepancies = reconciler.get_discrepancies(min_severity=args.min_severity)
        print_discrepancies(discrepancies, max_rows=args.max_rows)
        if args.export:
            path = reconciler.export_report(args.export, only_discrepancies=not args.full_report)
            console.print(f"\n[green]Report saved to:[/green] {path}")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise SystemExit(1)

if __name__ == "__main__":
    main()
