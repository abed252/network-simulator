import sys
import random


class Task:

    def __init__(self, start, duration, rate):
        self.start = start
        self.duration = duration
        self.rate = rate

    def remaining_time(self, current_time):
        return max(0, (self.start + self.duration) - current_time)


class QueueSimulator:

    def __init__(self, total_duration, server_count, arrival_rate, probabilities, capacities, service_rates):
        self.simulation_time = total_duration
        self.num_servers = server_count
        self.arrival_rate = arrival_rate
        self.server_probabilities = probabilities
        self.server_capacities = capacities
        self.service_rates = service_rates

        self.current_time = 0
        self.total_wait_time = 0
        self.total_service_time = 0
        self.final_time = total_duration
        self.accepted_tasks = 0
        self.rejected_tasks = 0
        self.queues = [[] for _ in range(server_count)]

    def simulate(self):
        while self.current_time < self.simulation_time:
            server_id = self.select_server()
            self.process_finished_tasks(server_id)
            self.schedule_task(server_id)
            self.current_time += self.generate_interarrival_time(self.arrival_rate)

        self.update_final_time()
        self.display_summary()

    def select_server(self):
        r = random.uniform(0, 1)
        cumulative = 0
        for index, prob in enumerate(self.server_probabilities):
            cumulative += prob
            if r < cumulative:
                return index
        return -1

    def process_finished_tasks(self, server_id):
        if server_id < 0:
            return
        self.queues[server_id] = [
            task for task in self.queues[server_id] if task.remaining_time(self.current_time) > 0
        ]

    def schedule_task(self, server_id):
        if server_id < 0:
            return

        queue_size = len(self.queues[server_id])
        max_capacity = self.server_capacities[server_id]

        if queue_size >= max_capacity:
            self.rejected_tasks += 1
            return

        service_rate = self.service_rates[server_id]
        processing_time = self.generate_interarrival_time(service_rate)
        start_time = self.current_time

        if queue_size > 0:
            last_task = self.queues[server_id][-1]
            start_time = max(self.current_time, last_task.start + last_task.duration)

        new_task = Task(start_time, processing_time, service_rate)
        self.queues[server_id].append(new_task)

        self.accepted_tasks += 1
        self.total_wait_time += max(0, start_time - self.current_time)
        self.total_service_time += processing_time

    def update_final_time(self):
        for server_queue in self.queues:
            for task in server_queue:
                self.final_time = max(self.final_time, task.start + task.duration)

    # Helper methods
    def generate_interarrival_time(self, rate):
        return random.expovariate(rate)

    def display_summary(self):
        avg_wait = self.total_wait_time / self.accepted_tasks if self.accepted_tasks > 0 else 0
        avg_service = self.total_service_time / self.accepted_tasks if self.accepted_tasks > 0 else 0
        print(f"{self.accepted_tasks} {self.rejected_tasks} {self.final_time:.4f} {avg_wait:.4f} {avg_service:.4f}")



def validate_input(arguments):


    total_time = float(arguments[0])
    if total_time <= 0:
        return

    num_servers = int(arguments[1])
    if num_servers <= 0:
        return

    probabilities = [float(arguments[i]) for i in range(2, 2 + num_servers)]
    if not abs(sum(probabilities) - 1.0) < 1e-6:
        return

    arrival_rate = float(arguments[2 + num_servers])
    if arrival_rate <= 0:
        return

    capacities = [int(arguments[i]) + 1 for i in range(3 + num_servers, 3 + 2 * num_servers)]
    if any(cap <= 0 for cap in capacities):
        return

    service_rates = [float(arguments[i]) for i in range(3 + 2 * num_servers, 3 + 3 * num_servers)]
    if any(rate <= 0 for rate in service_rates):
        return

    return total_time, num_servers, arrival_rate, probabilities, capacities, service_rates



def main():

    args = sys.argv[1:]
    total_time, num_servers, arrival_rate, probabilities, capacities, service_rates = validate_input(args)

    simulator = QueueSimulator(total_time, num_servers, arrival_rate, probabilities, capacities, service_rates)
    simulator.simulate()


if __name__ == "__main__":
    main()
