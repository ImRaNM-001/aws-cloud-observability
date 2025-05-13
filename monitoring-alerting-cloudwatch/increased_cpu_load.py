import time

def simulate_cpu_spike(duration, cpu_percent):
    print(f'Simulating CPU spike at {cpu_percent}% for {duration} seconds...')
    start_time = time.time()
    end_time = start_time + duration

    # Calculate busy and idle times per cycle (100ms cycle)
    cycle = 0.1  # seconds
    busy_time = cycle * (cpu_percent / 100)
    idle_time = cycle - busy_time

    while time.time() < end_time:
        cycle_start = time.time()

        # Busy-wait for busy_time
        while (time.time() - cycle_start) < busy_time:
            pass

        # Sleep for idle_time
        if idle_time > 0:
            time.sleep(idle_time)

    print('CPU spike simulation completed')

if __name__ == '__main__':
    # Simulate a CPU spike for 5 mins (300 seconds) or 10 mins (best) to avoid metric delay with 80% CPU utilization
    simulate_cpu_spike(duration = 300, cpu_percent = 80)