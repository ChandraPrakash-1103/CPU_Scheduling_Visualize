"""
CPU Scheduling Visualizer
-------------------------
Implements four CPU scheduling algorithms:

1. FCFS - First Come First Served
2. SJF - Shortest Job First (Non-Preemptive)
3. Priority Scheduling (Non-Preemptive)
4. Round Robin (Preemptive)

Features:
- Dynamic process input
- Arrival time support
- CPU idle time detection
- Gantt chart generation
- Completion time calculation
- Turnaround time calculation
- Waiting time calculation
- Response time calculation
- Input validation
- Stable scheduling order

Return format remains compatible with app.py:

results, gantt_chart, avg_waiting, avg_turnaround
"""

from collections import deque


# ============================================================
# 1. INPUT VALIDATION
# ============================================================

def validate_processes(processes):

    if not processes:
        raise ValueError(
            "Please enter at least one process."
        )

    jobs = []

    for index, process in enumerate(processes):

        if not isinstance(process, dict):
            raise ValueError(
                "Invalid process information."
            )

        try:
            pid = str(process["id"]).strip()

            arrival = int(process["arrival"])

            burst = int(process["burst"])

            priority = int(
                process.get("priority", 1)
            )

        except (KeyError, TypeError, ValueError):
            raise ValueError(
                "Please provide valid process information."
            )

        if not pid:
            raise ValueError(
                "Process ID cannot be empty."
            )

        if arrival < 0:
            raise ValueError(
                f"Arrival time of {pid} cannot be negative."
            )

        if burst <= 0:
            raise ValueError(
                f"Burst time of {pid} must be greater than zero."
            )

        if priority <= 0:
            raise ValueError(
                f"Priority of {pid} must be greater than zero."
            )

        jobs.append({

            "id": pid,

            "arrival": arrival,

            "burst": burst,

            "priority": priority,

            "order": index,

        })

    # Check duplicate process IDs

    process_ids = [
        process["id"] for process in jobs
    ]

    if len(process_ids) != len(set(process_ids)):

        raise ValueError(
            "Each process must have a unique Process ID."
        )

    return jobs


# ============================================================
# 2. GANTT CHART HELPER
# ============================================================

def add_gantt_entry(gantt_chart, pid, start, end):

    if end <= start:
        return

    gantt_chart.append({

        "id": pid,

        "start": start,

        "end": end,

    })


# ============================================================
# 3. FCFS SCHEDULING
# ============================================================

def fcfs_scheduling(jobs):

    remaining = jobs.copy()

    current_time = 0

    gantt_chart = []

    results = []

    while remaining:

        available = [

            process

            for process in remaining

            if process["arrival"] <= current_time

        ]

        # Handle CPU idle time

        if not available:

            next_arrival = min(

                process["arrival"]

                for process in remaining

            )

            add_gantt_entry(

                gantt_chart,

                "Idle",

                current_time,

                next_arrival

            )

            current_time = next_arrival

            available = [

                process

                for process in remaining

                if process["arrival"] <= current_time

            ]

        # Select earliest arriving process

        selected = min(

            available,

            key=lambda p: (

                p["arrival"],

                p["order"]

            )

        )

        start_time = current_time

        completion_time = (

            start_time + selected["burst"]

        )

        add_gantt_entry(

            gantt_chart,

            selected["id"],

            start_time,

            completion_time

        )

        turnaround_time = (

            completion_time - selected["arrival"]

        )

        waiting_time = (

            turnaround_time - selected["burst"]

        )

        response_time = (

            start_time - selected["arrival"]

        )

        results.append({

            "id": selected["id"],

            "arrival": selected["arrival"],

            "burst": selected["burst"],

            "priority": selected["priority"],

            "start": start_time,

            "completion": completion_time,

            "turnaround": turnaround_time,

            "waiting": waiting_time,

            "response": response_time,

        })

        current_time = completion_time

        remaining.remove(selected)

    return results, gantt_chart


# ============================================================
# 4. SJF SCHEDULING (NON-PREEMPTIVE)
# ============================================================

def sjf_scheduling(jobs):

    remaining = jobs.copy()

    current_time = 0

    gantt_chart = []

    results = []

    while remaining:

        available = [

            process

            for process in remaining

            if process["arrival"] <= current_time

        ]

        # Handle CPU idle time

        if not available:

            next_arrival = min(

                process["arrival"]

                for process in remaining

            )

            add_gantt_entry(

                gantt_chart,

                "Idle",

                current_time,

                next_arrival

            )

            current_time = next_arrival

            available = [

                process

                for process in remaining

                if process["arrival"] <= current_time

            ]

        # Select shortest available burst time

        selected = min(

            available,

            key=lambda p: (

                p["burst"],

                p["arrival"],

                p["order"]

            )

        )

        start_time = current_time

        completion_time = (

            start_time + selected["burst"]

        )

        add_gantt_entry(

            gantt_chart,

            selected["id"],

            start_time,

            completion_time

        )

        turnaround_time = (

            completion_time - selected["arrival"]

        )

        waiting_time = (

            turnaround_time - selected["burst"]

        )

        response_time = (

            start_time - selected["arrival"]

        )

        results.append({

            "id": selected["id"],

            "arrival": selected["arrival"],

            "burst": selected["burst"],

            "priority": selected["priority"],

            "start": start_time,

            "completion": completion_time,

            "turnaround": turnaround_time,

            "waiting": waiting_time,

            "response": response_time,

        })

        current_time = completion_time

        remaining.remove(selected)

    return results, gantt_chart


# ============================================================
# 5. PRIORITY SCHEDULING (NON-PREEMPTIVE)
# ============================================================

def priority_scheduling(jobs):

    remaining = jobs.copy()

    current_time = 0

    gantt_chart = []

    results = []

    while remaining:

        available = [

            process

            for process in remaining

            if process["arrival"] <= current_time

        ]

        # Handle CPU idle time

        if not available:

            next_arrival = min(

                process["arrival"]

                for process in remaining

            )

            add_gantt_entry(

                gantt_chart,

                "Idle",

                current_time,

                next_arrival

            )

            current_time = next_arrival

            available = [

                process

                for process in remaining

                if process["arrival"] <= current_time

            ]

        # Lower priority number means higher priority

        selected = min(

            available,

            key=lambda p: (

                p["priority"],

                p["arrival"],

                p["order"]

            )

        )

        start_time = current_time

        completion_time = (

            start_time + selected["burst"]

        )

        add_gantt_entry(

            gantt_chart,

            selected["id"],

            start_time,

            completion_time

        )

        turnaround_time = (

            completion_time - selected["arrival"]

        )

        waiting_time = (

            turnaround_time - selected["burst"]

        )

        response_time = (

            start_time - selected["arrival"]

        )

        results.append({

            "id": selected["id"],

            "arrival": selected["arrival"],

            "burst": selected["burst"],

            "priority": selected["priority"],

            "start": start_time,

            "completion": completion_time,

            "turnaround": turnaround_time,

            "waiting": waiting_time,

            "response": response_time,

        })

        current_time = completion_time

        remaining.remove(selected)

    return results, gantt_chart


# ============================================================
# 6. ROUND ROBIN SCHEDULING (PREEMPTIVE)
# ============================================================

def round_robin_scheduling(jobs, quantum):

    if quantum <= 0:

        raise ValueError(
            "Time quantum must be greater than zero."
        )

    # Sort processes according to arrival time

    sorted_jobs = sorted(

        jobs,

        key=lambda p: (

            p["arrival"],

            p["order"]

        )

    )

    remaining_time = {

        process["id"]: process["burst"]

        for process in sorted_jobs

    }

    first_start = {}

    completion_time = {}

    ready_queue = deque()

    gantt_chart = []

    current_time = 0

    next_process = 0

    total_processes = len(sorted_jobs)

    # Execute until every process is completed

    while (

        next_process < total_processes

        or ready_queue

    ):

        # If ready queue is empty, move to next arrival

        if not ready_queue:

            next_arrival = sorted_jobs[

                next_process

            ]["arrival"]

            if current_time < next_arrival:

                add_gantt_entry(

                    gantt_chart,

                    "Idle",

                    current_time,

                    next_arrival

                )

            current_time = max(

                current_time,

                next_arrival

            )

            # Add all arrived processes to ready queue

            while (

                next_process < total_processes

                and sorted_jobs[next_process]["arrival"]

                <= current_time

            ):

                ready_queue.append(

                    sorted_jobs[next_process]

                )

                next_process += 1

        # Select the next process

        process = ready_queue.popleft()

        pid = process["id"]

        # Record first CPU execution time

        if pid not in first_start:

            first_start[pid] = current_time

        # Execute process for one time quantum

        execution_time = min(

            quantum,

            remaining_time[pid]

        )

        start_time = current_time

        end_time = current_time + execution_time

        add_gantt_entry(

            gantt_chart,

            pid,

            start_time,

            end_time

        )

        current_time = end_time

        remaining_time[pid] -= execution_time

        # Add newly arrived processes

        while (

            next_process < total_processes

            and sorted_jobs[next_process]["arrival"]

            <= current_time

        ):

            ready_queue.append(

                sorted_jobs[next_process]

            )

            next_process += 1

        # Requeue unfinished process

        if remaining_time[pid] > 0:

            ready_queue.append(process)

        else:

            completion_time[pid] = current_time

    results = []

    # Calculate final metrics for every process

    for process in sorted_jobs:

        pid = process["id"]

        arrival = process["arrival"]

        burst = process["burst"]

        completion = completion_time[pid]

        start = first_start[pid]

        turnaround = completion - arrival

        waiting = turnaround - burst

        response = start - arrival

        results.append({

            "id": pid,

            "arrival": arrival,

            "burst": burst,

            "priority": process["priority"],

            "start": start,

            "completion": completion,

            "turnaround": turnaround,

            "waiting": waiting,

            "response": response,

        })

    return results, gantt_chart


# ============================================================
# 7. MAIN SCHEDULING FUNCTION
# ============================================================

def schedule_processes(processes, algorithm, quantum=2):

    """
    Execute the selected CPU scheduling algorithm.

    Parameters
    ----------
    processes : list
        List of process dictionaries containing:
        id, arrival, burst, priority.

    algorithm : str
        FCFS, SJF, Priority, or RR.

    quantum : int
        Time quantum used by Round Robin.

    Returns
    -------
    results : list
        Individual process execution metrics.

    gantt_chart : list
        CPU execution timeline.

    avg_waiting : float
        Average waiting time.

    avg_turnaround : float
        Average turnaround time.
    """

    # Validate algorithm

    valid_algorithms = [

        "FCFS",

        "SJF",

        "Priority",

        "RR"

    ]

    if algorithm not in valid_algorithms:

        raise ValueError(
            "Unknown scheduling algorithm. "
            "Choose FCFS, SJF, Priority, or RR."
        )

    # Validate process information

    jobs = validate_processes(processes)

    # Validate quantum for Round Robin

    if algorithm == "RR":

        try:

            quantum = int(quantum)

        except (TypeError, ValueError):

            raise ValueError(
                "Time quantum must be a valid whole number."
            )

        if quantum <= 0:

            raise ValueError(
                "Time quantum must be greater than zero."
            )

    # Execute selected algorithm

    if algorithm == "FCFS":

        results, gantt_chart = fcfs_scheduling(jobs)

    elif algorithm == "SJF":

        results, gantt_chart = sjf_scheduling(jobs)

    elif algorithm == "Priority":

        results, gantt_chart = priority_scheduling(jobs)

    elif algorithm == "RR":

        results, gantt_chart = round_robin_scheduling(

            jobs,

            quantum

        )

    # Sort result rows in original input order

    original_order = {

        process["id"]: process["order"]

        for process in jobs

    }

    results.sort(

        key=lambda p: original_order[p["id"]]

    )

    # Calculate average waiting time

    avg_waiting = (

        sum(

            process["waiting"]

            for process in results

        ) / len(results)

    )

    # Calculate average turnaround time

    avg_turnaround = (

        sum(

            process["turnaround"]

            for process in results

        ) / len(results)

    )

    # Return values compatible with app.py

    return (

        results,

        gantt_chart,

        avg_waiting,

        avg_turnaround

    )


# ============================================================
# END OF SCHEDULER MODULE
# ============================================================