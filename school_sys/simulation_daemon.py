
import os
import sys
import time
import requests
import random
import threading
from datetime import datetime, timedelta, date
from decimal import Decimal
from unittest.mock import patch

# Configure Django Environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_sys.settings')

try:
    import django
    django.setup()
    from django.conf import settings
    from django.utils import timezone
    # Import Cron Logic
    from cron_colegiaturas_mensuales import generar_colegiaturas
    from cron_adeudos_vencidos import procesar_adeudos_vencidos
    from cron_reinscripcion import procesar_reinscripciones
except ImportError as e:
    print(f"Error importing Django modules: {e}")
    sys.exit(1)

# CONSTANTS
API_BASE_URL = "http://127.0.0.1:8000"
REAL_SECONDS_PER_SIM_DAY = 5  # Accelerate for demo: 5 real seconds = 1 sim day (approx 1 minute = 12 days)
# REAL_SECONDS_PER_SIM_DAY = 473 # Proper pacing: ~8 mins = 1 day (2 days = 1 year)

class MockTimezone:
    def __init__(self, start_date):
        self.current_sim_time = datetime.combine(start_date, datetime.min.time())
        self.real_start_time = time.time()
    
    def now(self):
        return timezone.make_aware(self.current_sim_time)
    
    def localdate(self):
        return self.current_sim_time.date()
    
    def update(self):
        elapsed_real = time.time() - self.real_start_time
        days_passed = elapsed_real / REAL_SECONDS_PER_SIM_DAY
        self.current_sim_time = datetime.combine(date(2024, 8, 1), datetime.min.time()) + timedelta(days=days_passed)
        return self.current_sim_time.date()

class SimulationEngine:
    def __init__(self):
        self.time_manager = MockTimezone(date(2024, 8, 1))
        self.last_sim_date = self.time_manager.localdate()
        self.tokens = {}
        # Pre-defined users from simulation_script.py
        self.users = [
            {'email': 'maestro0@sms.edu', 'password': 'pass123', 'role': 'maestro'},
            {'email': 'alumno0@sms.edu', 'password': 'pass123', 'role': 'estudiante'}
        ]

    def log(self, message):
        sim_date_str = self.time_manager.localdate().strftime("%Y-%m-%d")
        print(f"[{sim_date_str}] {message}")

    def login_user(self, email, password):
        try:
            resp = requests.post(f"{API_BASE_URL}/api/token/", data={'email': email, 'password': password}, timeout=5)
            if resp.status_code == 200:
                self.log(f"Login success: {email}")
                return resp.json()['access']
            else:
                self.log(f"Login failed: {email} ({resp.status_code})")
        except Exception as e:
            self.log(f"Login exception: {email} - {e}")
        return None

    def simulate_api_activity(self):
        user = random.choice(self.users)
        token = self.tokens.get(user['email'])
        
        if not token:
            token = self.login_user(user['email'], user['password'])
            if token:
                self.tokens[user['email']] = token
        
        if token:
            headers = {'Authorization': f'Bearer {token}'}
            try:
                if user['role'] == 'estudiante':
                    # View Profile
                    requests.get(f"{API_BASE_URL}/students/info/", headers=headers, timeout=5)
                    # View Grades
                    requests.get(f"{API_BASE_URL}/academico/api/estudiante/historial/", headers=headers, timeout=5)
                elif user['role'] == 'maestro':
                    # View Assignments
                    requests.get(f"{API_BASE_URL}/academico/api/maestro/asignaciones/", headers=headers, timeout=5)
            except Exception:
                pass

    def run_daily_tasks(self):
        current_date = self.time_manager.localdate()
        self.log(f"--- New Simulated Day: {current_date} ---")

        # Patch timezone for the specific cron functions
        with patch('django.utils.timezone.now', side_effect=self.time_manager.now), \
             patch('django.utils.timezone.localdate', side_effect=self.time_manager.localdate):
            
            # 1. Adeudos Vencidos (Daily)
            try:
                procesar_adeudos_vencidos()
                self.log("Processed overdue debts.")
            except Exception as e:
                self.log(f"Error calling adeudos_vencidos: {e}")

            # 2. Monthly Colegiaturas (Day 1)
            if current_date.day == 1:
                self.log("First of month: Generating tuition fees...")
                try:
                    generar_colegiaturas()
                    self.log("Tuition fees generated.")
                except Exception as e:
                    self.log(f"Error calling colegiaturas: {e}")

            # 3. Reinscription (End of Cycle - July 15)
            if current_date.month == 7 and current_date.day == 15:
                self.log("End of cycle detected. Processing reinscriptions...")
                try:
                    procesar_reinscripciones()
                    self.log("Reinscriptions processed.")
                except Exception as e:
                    self.log(f"Error calling reinscripcion: {e}")

    def run(self):
        self.log(f"Starting simulation daemon. 1 Simulated Day = {REAL_SECONDS_PER_SIM_DAY} Real Seconds.")
        self.log("Press Ctrl+C to stop.")
        
        while True:
            current_sim_date = self.time_manager.update()
            
            if current_sim_date > self.last_sim_date:
                # Catch up on missed days if simulation jumps
                while self.last_sim_date < current_sim_date:
                    self.last_sim_date += timedelta(days=1)
                    # Temporarily update the mock time for the catch-up day
                    self.time_manager.current_sim_time = datetime.combine(self.last_sim_date, datetime.min.time())
                    self.run_daily_tasks()
                
                # Restore current time
                self.time_manager.update()

            # Background API activity
            if random.random() < 0.2:
                threading.Thread(target=self.simulate_api_activity).start()

            time.sleep(1)

if __name__ == "__main__":
    engine = SimulationEngine()
    try:
        engine.run()
    except KeyboardInterrupt:
        print("\nSimulation stopped.")
