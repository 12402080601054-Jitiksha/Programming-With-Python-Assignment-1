import heapq
import sys


class Job:
    """Stores information about one job."""

    def __init__(self, arrival_time, job_id, priority, duration, resources, order):
        self.arrival_time = arrival_time
        self.job_id = job_id
        self.priority = priority
        self.duration = duration
        self.resources = resources
        self.order = order


def read_input():
    """Read and validate all input data."""

    first_line = input().split()

    if len(first_line) != 2:
        raise ValueError("First line must contain worker count and job count.")

    w, n = map(int, first_line)

    if not (1 <= w <= 64):
        raise ValueError("Number of workers must be between 1 and 64.")

    if not (1 <= n <= 200000):
        raise ValueError("Number of jobs must be between 1 and 200000.")

    jobs = []

    for order in range(n):
        parts = input().split()

        if len(parts) != 5:
            raise ValueError("Each job must contain 5 values.")

        arrival_time = int(parts[0])
        job_id = parts[1]
        priority = int(parts[2])
        duration = int(parts[3])
        resources = int(parts[4])

        if arrival_time < 0:
            raise ValueError("Arrival time cannot be negative.")

        if duration < 1 or duration > 10**6:
            raise ValueError("Invalid duration.")

        if resources < 1 or resources > 100:
            raise ValueError("Invalid resource count.")

        jobs.append(
            Job(
                arrival_time,
                job_id,
                priority,
                duration,
                resources,
                order
            )
        )

    return w, jobs


def simulate_scheduler(worker_count, jobs):
    """
    Simulate the job scheduler.

    Waiting jobs are stored in a priority queue:
        - Higher priority first
        - Earlier arrival time first
        - Earlier input order for exact ties

    Workers are stored in a min-heap so that the worker that becomes
    available first is selected.
    """

    # Sort jobs by arrival time.
    jobs.sort(key=lambda job: (job.arrival_time, job.order))

    # Worker heap:
    # (available_time, worker_number)
    #
    # Initially every worker is available at time 0.
    worker_heap = [
        (0, worker_id)
        for worker_id in range(1, worker_count + 1)
    ]

    heapq.heapify(worker_heap)

    # Waiting job priority queue.
    #
    # Python heap is a min-heap, so priority is stored as negative.
    waiting_heap = []

    results = []

    job_index = 0
    current_time = 0

    while job_index < len(jobs) or waiting_heap:

        # Add all jobs that have arrived by current_time.
        while (
            job_index < len(jobs)
            and jobs[job_index].arrival_time <= current_time
        ):
            job = jobs[job_index]

            heapq.heappush(
                waiting_heap,
                (
                    -job.priority,
                    job.arrival_time,
                    job.order,
                    job
                )
            )

            job_index += 1

        # If there are no waiting jobs, move time to the next arrival.
        if not waiting_heap:
            if job_index < len(jobs):
                current_time = max(
                    current_time,
                    jobs[job_index].arrival_time
                )
                continue

        # Get the earliest available worker.
        available_time, worker_id = heapq.heappop(worker_heap)

        # The worker may become available after current_time.
        if available_time > current_time:
            current_time = available_time

            # Add jobs that arrived while the worker was busy.
            while (
                job_index < len(jobs)
                and jobs[job_index].arrival_time <= current_time
            ):
                job = jobs[job_index]

                heapq.heappush(
                    waiting_heap,
                    (
                        -job.priority,
                        job.arrival_time,
                        job.order,
                        job
                    )
                )

                job_index += 1

        # If no job is currently waiting, return worker to heap.
        if not waiting_heap:
            heapq.heappush(
                worker_heap,
                (available_time, worker_id)
            )
            continue

        # Select highest-priority waiting job.
        _, _, _, job = heapq.heappop(waiting_heap)

        start_time = max(current_time, job.arrival_time)
        finish_time = start_time + job.duration

        results.append(
            (
                job.order,
                job.job_id,
                worker_id,
                start_time,
                finish_time,
                start_time - job.arrival_time
            )
        )

        # Worker becomes available after this job.
        heapq.heappush(
            worker_heap,
            (finish_time, worker_id)
        )

        current_time = start_time

    # Restore original input order for final report.
    results.sort(key=lambda result: result[0])

    return results


def print_results(results):
    """Print execution report and average waiting time."""

    total_waiting_time = 0

    for (
        order,
        job_id,
        worker_id,
        start_time,
        finish_time,
        waiting_time
    ) in results:

        print(
            f"{job_id} W{worker_id} "
            f"{start_time} {finish_time}"
        )

        total_waiting_time += waiting_time

    average_wait = total_waiting_time / len(results)

    print(f"AVG_WAIT {average_wait:.2f}")


def main():
    """Main program."""

    try:
        worker_count, jobs = read_input()

        results = simulate_scheduler(
            worker_count,
            jobs
        )

        print_results(results)

    except ValueError as error:
        print(f"INVALID: {error}")
    except EOFError:
        print("INVALID: Incomplete input")


if __name__ == "__main__":
    main()