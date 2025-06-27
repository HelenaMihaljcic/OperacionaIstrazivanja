import pulp
import time
import json

class ShiftScheduler:
    """
    Klasa za modelovanje i rješavanje problema raspoređivanja smjena
    pomoću linearnog programiranja (PuLP).
    """
    def __init__(self, instance_id, big_M=10000):
        """
        Inicijalizuje scheduler sa ID-jem instance i velikim M koeficijentom za slack varijable.
        """
        self.instance_id = instance_id
        self.big_M = big_M
        self.employees = {}
        self.shifts = {}
        self.days = []
        self.model = None
        self.x = None
        self.slack = None

    def _load_data(self):
        """Učitava podatke za instancu iz JSON fajla."""
        with open(f"instance_{self.instance_id}.json") as f:
            data = json.load(f)
        self.employees = data["employees"]
        self.shifts = data["shifts"]
        self.days = data["days"]

    def _create_model(self):
        """Inicijalizuje PuLP model i varijable."""
        self.model = pulp.LpProblem("Shift_Scheduling", pulp.LpMinimize)
        
        self.x = pulp.LpVariable.dicts(
            "x",
            [(e, d, s) for e in self.employees for d in self.days for s in self.shifts if s in self.employees[e]["availability"][d]],
            cat="Binary"
        )
        
        self.slack = pulp.LpVariable.dicts(
            "slack",
            [(d, s) for d in self.days for s in self.shifts],
            lowBound=0,
            cat="Integer"
        )

    def _set_objective(self):
        """Postavlja funkciju cilja: minimizacija ukupnih troškova rada."""
        self.model += (
            pulp.lpSum(
                self.x[e, d, s] * self.employees[e]["rate"] * self.shifts[s]["duration"]
                for e, d, s in self.x
            )
            + self.big_M * pulp.lpSum(self.slack[d, s] for d in self.days for s in self.shifts),
            "Ukupni_Troškovi"
        )

    def _add_all_constraints(self):
        """Dodaje sva ograničenja modelu."""
        for d in self.days:
            for s in self.shifts:
                available_employees_for_shift = [e for e in self.employees if s in self.employees[e]["availability"][d]]
                self.model += (
                    pulp.lpSum(self.x[e, d, s] for e in available_employees_for_shift if (e, d, s) in self.x) + self.slack[d, s] >= self.shifts[s]["required"],
                    f"Pokrivenost_smjene_{d}_{s}"
                )

        for e in self.employees:
            for d in self.days:
                self.model += pulp.lpSum(
                    self.x[e, d, s] for s in self.shifts if (e, d, s) in self.x
                ) <= 1, f"Max_jedna_smjena_dnevno_{e}_{d}"

        for e in self.employees:
            self.model += pulp.lpSum(
                self.x[e, d, s] * self.shifts[s]["duration"]
                for d in self.days for s in self.shifts if (e, d, s) in self.x
            ) <= self.employees[e]["max_hours"], f"Max_sati_nedjeljno_{e}"

    def solve(self):
        """Rješava PuLP model i vraća model i vrijeme izvršenja."""
        self._load_data()
        self._create_model()
        self._set_objective()
        self._add_all_constraints()

        start_time = time.time()
        solver = pulp.PULP_CBC_CMD(msg=False, timeLimit=300)
        self.model.solve(solver)
        end_time = time.time()

        return self.model, end_time - start_time

def run_pulp(instance_id):
    """
    Pomoćna funkcija za pokretanje PuLP rješavača.
    """
    scheduler = ShiftScheduler(instance_id)
    return scheduler.solve()