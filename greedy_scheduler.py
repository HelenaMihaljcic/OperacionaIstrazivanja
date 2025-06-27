import time
from collections import defaultdict

def greedy_scheduler(employees, shifts, days):
    """
    Implementira pohlepni algoritam za raspoređivanje smjena.
    Pokušava dodijeliti najjeftinije zaposlene najjeftinijim smjenama.

    Parametri:
        employees (dict): Rječnik zaposlenih sa njihovim detaljima.
        shifts (dict): Rječnik smjena sa njihovim detaljima.
        days (list): Lista dana u nedelji.

    Vraća:
        tuple: (ukupni_trošak, raspored) ili (float('inf'), None) ako nije moguće pokriti sve smjene.
    """
    schedule = defaultdict(list)
    remaining_hours = {e: employees[e]["max_hours"] for e in employees}
    total_cost = 0

    avg_rate = sum(emp_data["rate"] for emp_data in employees.values()) / len(employees) if employees else 0
    shift_costs_heuristic = {s: shifts[s]["duration"] * avg_rate for s in shifts}
    sorted_shifts = sorted(shifts.keys(), key=lambda s: shift_costs_heuristic[s])

    for day in days:
        daily_assigned = {e: False for e in employees} 
        for s_name in sorted_shifts:
            needed = shifts[s_name]["required"]
            duration = shifts[s_name]["duration"]
            
            assigned_count = 0
            
            candidates = sorted(
                [
                    emp for emp in employees
                    if s_name in employees[emp]["availability"][day]
                    and remaining_hours[emp] >= duration
                    and not daily_assigned[emp]
                ],
                key=lambda emp: employees[emp]["rate"]
            )

            for emp in candidates:
                if assigned_count >= needed:
                    break
                
                schedule[emp].append((day, s_name))
                remaining_hours[emp] -= duration
                total_cost += employees[emp]["rate"] * duration
                daily_assigned[emp] = True
                assigned_count += 1

            if assigned_count < needed:
                return float('inf'), None

    return total_cost, schedule