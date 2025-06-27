import time
import json
import pulp

def load_instance_data(instance_id):
    with open(f"instance_{instance_id}.json") as f:
        return json.load(f)

def run_pulp_solver(instance_id):
    pulp_model, pulp_time_s = run_pulp(instance_id)
    pulp_time_ms = pulp_time_s * 1000
    pulp_cost = pulp.value(pulp_model.objective) if pulp_model.status == 1 else float('inf')
    return pulp_cost, pulp_time_ms, pulp_time_s

def run_greedy_solver(employees, shifts, days):
    start_greedy = time.time()
    greedy_cost, _ = greedy_scheduler(employees, shifts, days)
    greedy_time_s = time.time() - start_greedy
    greedy_time_ms = greedy_time_s * 1000
    return greedy_cost, greedy_time_ms, greedy_time_s

def test_instance_refactored(instance_id):
    data = load_instance_data(instance_id)

    pulp_cost, pulp_time_ms, pulp_time_s = run_pulp_solver(instance_id)
    greedy_cost, greedy_time_ms, greedy_time_s = run_greedy_solver(data["employees"], data["shifts"], data["days"])
    
    return {
        "instance": instance_id,
        "satnica": data["instance_info"]["rate_range"],
        "sati": data["instance_info"]["hours_range"],
        "pulp_cost": pulp_cost,
        "pulp_time": f"{pulp_time_ms:.2f} ms / {pulp_time_s:.3f} s",
        "greedy_cost": greedy_cost,
        "greedy_time": f"{greedy_time_ms:.2f} ms / {greedy_time_s:.3f} s"
    }

def print_results_table_refactored(results):
    print("\n=== REZULTATI ===")
    print(f"{'Instanca':<10} | {'Satnica ($)':<15} | {'Max sati (h)':<15} | "
          f"{'PuLP Trošak (USD)':<20} | {'Pohlepni Trošak (USD)':<20} | "
          f"{'PuLP Vrijeme':<25} | {'Pohlepni Vrijeme':<25}")
    print("-" * 140)

    for res in results:
        pulp_cost = f"{res['pulp_cost']:.2f}" if res['pulp_cost'] != float('inf') else "Neizvodljivo"
        greedy_cost = f"{res['greedy_cost']:.2f}" if res['greedy_cost'] != float('inf') else "Neizvodljivo"

        print(
            f"{res['instance']:<10} | "
            f"{res['satnica']:<15} | "
            f"{res['sati']:<15} | "
            f"{pulp_cost:<20} | "
            f"{greedy_cost:<20} | "
            f"{res['pulp_time']:<25} | "
            f"{res['greedy_time']:<25}"
        )

if __name__ == "__main__":
    from scheduler_ import run_pulp 
    from greedy_scheduler import greedy_scheduler 

    results = []
    for i in [1, 2, 3]:
        print("nesto")
        results.append(test_instance_refactored(i))
    
    print_results_table_refactored(results)