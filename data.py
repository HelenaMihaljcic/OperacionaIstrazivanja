import random
import json

def generate_instance(instance_id, num_employees, min_rate_val=10, max_rate_val=35, min_hours_val=8, max_hours_val=25, min_shift_req_factor=0.2, max_shift_req_factor=0.5):
    """
    Generiše JSON fajl sa podacima za instancu problema rasporeda.

    Parametri:
        instance_id (int): Jedinstveni ID instance.
        num_employees (int): Broj zaposlenih koje treba generisati.
        min_rate_val (int): Minimalna satnica za zaposlene.
        max_rate_val (int): Maksimalna satnica za zaposlene.
        min_hours_val (int): Minimalni maksimalni nedeljni sati za zaposlene.
        max_hours_val (int): Maksimalni maksimalni nedeljni sati za zaposlene.
        min_shift_req_factor (float): Minimalni faktor za određivanje potrebnog broja zaposlenih po smjeni.
        max_shift_req_factor (float): Maksimalni faktor za određivanje potrebnog broja zaposlenih po smjeni.
    """
    days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    employees = {}
    shifts = {}

  
    min_rate_actual = float('inf')
    max_rate_actual = float('-inf')
    min_hours_actual = float('inf')
    max_hours_actual = float('-inf')

    
    for i in range(1, num_employees + 1):
        rate = random.randint(min_rate_val, max_rate_val)
        hours = random.randint(min_hours_val, max_hours_val)

        emp_name = f"Emp_{i}"
        employees[emp_name] = {
            "rate": rate,
            "max_hours": hours,
            "availability": {} 
        }
        for day in days:
            available_shifts_for_day = []
            if random.random() > 0.1: 
                available_shifts_for_day.append("morning")
            if random.random() > 0.1:
                available_shifts_for_day.append("afternoon")
            if random.random() > 0.4: 
                available_shifts_for_day.append("evening")
            

            if not available_shifts_for_day:
                 available_shifts_for_day.append(random.choice(["morning", "afternoon", "evening"]))

            employees[emp_name]["availability"][day] = available_shifts_for_day

        
        min_rate_actual = min(min_rate_actual, rate)
        max_rate_actual = max(max_rate_actual, rate)
        min_hours_actual = min(min_hours_actual, hours)
        max_hours_actual = max(max_hours_actual, hours)


    shifts["morning"] = {"duration": 4, "required": 0}
    shifts["afternoon"] = {"duration": 6, "required": 0}
    shifts["evening"] = {"duration": 4, "required": 0}

    def get_required(shift_type):
        """
        Izračunava potreban broj zaposlenih za smjenu na osnovu prosječne dnevne dostupnosti.
        """
        avg_daily_available = sum(
            sum(1 for emp_name, emp_data in employees.items() if shift_type in emp_data["availability"][day])
            for day in days
        ) / len(days)
        return max(1, int(avg_daily_available * random.uniform(min_shift_req_factor, max_shift_req_factor)))


    shifts["morning"]["required"] = get_required("morning")
    shifts["afternoon"]["required"] = get_required("afternoon")
    shifts["evening"]["required"] = get_required("evening")

    for day in days:
        for shift_name, shift_data in shifts.items():
            current_available_count = sum(1 for e in employees if shift_name in employees[e]["availability"][day])
            while current_available_count < shift_data["required"]:
                emp_to_update = random.choice(list(employees.keys()))
                if shift_name not in employees[emp_to_update]["availability"][day]:
                    employees[emp_to_update]["availability"][day].append(shift_name)
                    employees[emp_to_update]["availability"][day].sort() 
                    current_available_count += 1

    with open(f"instance_{instance_id}.json", "w") as f:
        json.dump({
            "employees": employees,
            "shifts": shifts,
            "days": days,
            "instance_info": { 
                "num_employees": num_employees,
                "rate_range": f"{min_rate_actual}-{max_rate_actual}",
                "hours_range": f"{min_hours_actual}-{max_hours_actual}",
                "morning_required": shifts["morning"]["required"],
                "afternoon_required": shifts["afternoon"]["required"],
                "evening_required": shifts["evening"]["required"]
            }
        }, f, indent=2)

if __name__ == "__main__":
    # Primjer generisanja instanci kada se ovaj fajl pokrene direktno
    print("Generisanje instanci pomoću data.py...")
    generate_instance(1, num_employees=100)
    #generate_instance(2, num_employees=500)
   # generate_instance(3, num_employees=1000)
    print("Generisanje instanci završeno.")