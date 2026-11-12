"""
CPU SCHEDULING VISUALIZER
Department of Computer Science & Engineering

Backend Application using Flask

Scheduling Algorithms:
1. FCFS
2. SJF
3. Priority Scheduling
4. Round Robin

Features:
- Process Management
- CPU Scheduling Simulation
- Gantt Chart Generation
- Performance Metrics
- Algorithm Comparison
- Automatic Result Analysis
- Input Validation
"""

import os
import subprocess
import threading
import webbrowser

from flask import Flask, render_template, request

from scheduler import schedule_processes


# ============================================================
# 1. APPLICATION CONFIGURATION
# ============================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "cpu-scheduling-visualizer"
)

ALLOWED_COUNTS = [3, 5, 8, 10, 15]

ALGORITHMS = [
    "FCFS",
    "SJF",
    "Priority",
    "RR"
]

DEFAULT_QUANTUM = 2


# ============================================================
# 2. DEFAULT PROCESS GENERATION
# ============================================================

def default_processes(count):

    return [

        {
            "id": f"P{i + 1}",
            "arrival": 0,
            "burst": i + 1,
            "priority": i + 1
        }

        for i in range(count)

    ]


# ============================================================
# 3. INPUT VALIDATION
# ============================================================

def parse_int(raw, label, minimum=None):

    try:

        value = int(str(raw).strip())

    except (TypeError, ValueError):

        raise ValueError(
            f"{label} must be a valid whole number."
        )

    if minimum is not None and value < minimum:

        raise ValueError(
            f"{label} must be at least {minimum}."
        )

    return value


# ============================================================
# 4. PROCESS DEFAULT HANDLING
# ============================================================

def fill_with_defaults(process_values, count):

    used = {

        p["id"]

        for p in process_values

    }

    defaults = default_processes(count)

    next_num = 1

    for template in defaults[len(process_values):]:

        while f"P{next_num}" in used:

            next_num += 1

        new_id = f"P{next_num}"

        used.add(new_id)

        process_values.append({

            **template,

            "id": new_id

        })

    return process_values


# ============================================================
# 5. PERFORMANCE METRIC CALCULATION
# ============================================================

def summarize_schedule(processes, algorithm, quantum):

    """
    Execute one scheduling algorithm and calculate
    all performance metrics.
    """

    rows, chart, avg_waiting, avg_turnaround = (
        schedule_processes(
            processes,
            algorithm,
            quantum
        )
    )

    # --------------------------------------------------------
    # Total CPU Burst Time
    # --------------------------------------------------------

    total_burst = sum(

        row["burst"]

        for row in rows

    )

    # --------------------------------------------------------
    # Total Execution Time
    # --------------------------------------------------------

    makespan = max(

        (entry["end"] for entry in chart),

        default=0

    )

    # --------------------------------------------------------
    # Average Response Time
    # --------------------------------------------------------

    avg_response = (

        sum(

            row["response"]

            for row in rows

        ) / len(rows)

        if rows else 0

    )

    # --------------------------------------------------------
    # CPU Utilization
    # --------------------------------------------------------

    cpu_utilization = (

        (total_burst / makespan) * 100

        if makespan > 0 else 0

    )

    # --------------------------------------------------------
    # CPU Idle Time
    # --------------------------------------------------------

    idle_time = sum(

        entry["end"] - entry["start"]

        for entry in chart

        if entry["id"] == "Idle"

    )

    # --------------------------------------------------------
    # Throughput
    # --------------------------------------------------------

    throughput = (

        len(rows) / makespan

        if makespan > 0 else 0

    )

    # --------------------------------------------------------
    # Return Complete Results
    # --------------------------------------------------------

    return {

        "algorithm": algorithm,

        "avg_waiting": avg_waiting,

        "avg_turnaround": avg_turnaround,

        "avg_response": avg_response,

        "utilization": cpu_utilization,

        "idle_time": idle_time,

        "throughput": throughput,

        "total_burst": total_burst,

        "makespan": makespan,

        "results": rows,

        "gantt_chart": chart

    }


# ============================================================
# 6. COMPARATIVE ANALYSIS
# ============================================================

def compare_algorithms(processes, quantum):

    """
    Execute all four algorithms using identical inputs.
    """

    comparison_results = []

    for algorithm in ALGORITHMS:

        result = summarize_schedule(

            processes,

            algorithm,

            quantum

        )

        comparison_results.append(result)

    return comparison_results


# ============================================================
# 7. AUTOMATIC OBSERVATION AND ANALYSIS
# ============================================================

def generate_observations(comparison_results):

    """
    Generate observations from actual simulation results.
    """

    if not comparison_results:

        return []

    observations = []

    # --------------------------------------------------------
    # Lowest Average Waiting Time
    # --------------------------------------------------------

    best_waiting = min(

        comparison_results,

        key=lambda x: x["avg_waiting"]

    )

    observations.append({

        "title": "Lowest Average Waiting Time",

        "algorithm": best_waiting["algorithm"],

        "value": round(
            best_waiting["avg_waiting"], 2
        ),

        "description": (

            f'{best_waiting["algorithm"]} achieved the lowest '
            f'average waiting time of '
            f'{best_waiting["avg_waiting"]:.2f} time units.'

        )

    })

    # --------------------------------------------------------
    # Lowest Average Turnaround Time
    # --------------------------------------------------------

    best_turnaround = min(

        comparison_results,

        key=lambda x: x["avg_turnaround"]

    )

    observations.append({

        "title": "Lowest Average Turnaround Time",

        "algorithm": best_turnaround["algorithm"],

        "value": round(
            best_turnaround["avg_turnaround"], 2
        ),

        "description": (

            f'{best_turnaround["algorithm"]} achieved the lowest '
            f'average turnaround time of '
            f'{best_turnaround["avg_turnaround"]:.2f} time units.'

        )

    })

    # --------------------------------------------------------
    # Lowest Average Response Time
    # --------------------------------------------------------

    best_response = min(

        comparison_results,

        key=lambda x: x["avg_response"]

    )

    observations.append({

        "title": "Lowest Average Response Time",

        "algorithm": best_response["algorithm"],

        "value": round(
            best_response["avg_response"], 2
        ),

        "description": (

            f'{best_response["algorithm"]} achieved the lowest '
            f'average response time of '
            f'{best_response["avg_response"]:.2f} time units.'

        )

    })

    # --------------------------------------------------------
    # Highest CPU Utilization
    # --------------------------------------------------------

    best_utilization = max(

        comparison_results,

        key=lambda x: x["utilization"]

    )

    observations.append({

        "title": "Highest CPU Utilization",

        "algorithm": best_utilization["algorithm"],

        "value": round(
            best_utilization["utilization"], 2
        ),

        "description": (

            f'{best_utilization["algorithm"]} achieved the highest '
            f'CPU utilization of '
            f'{best_utilization["utilization"]:.2f}%.'

        )

    })

    # --------------------------------------------------------
    # Highest Throughput
    # --------------------------------------------------------

    best_throughput = max(

        comparison_results,

        key=lambda x: x["throughput"]

    )

    observations.append({

        "title": "Highest Throughput",

        "algorithm": best_throughput["algorithm"],

        "value": round(
            best_throughput["throughput"], 4
        ),

        "description": (

            f'{best_throughput["algorithm"]} achieved the highest '
            f'throughput of '
            f'{best_throughput["throughput"]:.4f} processes '
            f'per time unit.'

        )

    })

    return observations


# ============================================================
# 8. MAIN APPLICATION ROUTE
# ============================================================

@app.route("/", methods=["GET", "POST"])
def home():

    # --------------------------------------------------------
    # Default Output Values
    # --------------------------------------------------------

    results = []

    gantt_chart = []

    comparison_results = []

    observations = []

    avg_waiting = 0

    avg_turnaround = 0

    avg_response = 0

    utilization = 0

    throughput = 0

    idle_time = 0

    makespan = 0

    error = None

    calculated = False

    compared = False

    algorithm = "FCFS"

    quantum = DEFAULT_QUANTUM

    process_count = 3

    process_values = default_processes(process_count)

    # --------------------------------------------------------
    # POST REQUEST
    # --------------------------------------------------------

    if request.method == "POST":

        algorithm = request.form.get(

            "algorithm",

            "FCFS"

        )

        action = request.form.get(

            "action",

            "calculate"

        )

        try:

            # ------------------------------------------------
            # Validate Selected Algorithm
            # ------------------------------------------------

            if algorithm not in ALGORITHMS:

                raise ValueError(
                    "Please select a valid scheduling algorithm."
                )

            # ------------------------------------------------
            # Validate Action
            # ------------------------------------------------

            if action not in ("calculate", "compare"):

                raise ValueError(
                    "Invalid operation selected."
                )

            # ------------------------------------------------
            # Validate Process Count
            # ------------------------------------------------

            process_count = parse_int(

                request.form.get(
                    "process_count",
                    3
                ),

                "Number of processes",

                minimum=1

            )

            if process_count not in ALLOWED_COUNTS:

                raise ValueError(

                    "Please select a valid process count: "

                    + ", ".join(
                        map(str, ALLOWED_COUNTS)
                    )

                )

            # ------------------------------------------------
            # Validate Time Quantum
            # ------------------------------------------------

            raw_quantum = request.form.get(

                "quantum",

                DEFAULT_QUANTUM

            )

            if algorithm == "RR" or action == "compare":

                quantum = parse_int(

                    raw_quantum,

                    "Time quantum",

                    minimum=1

                )

            else:

                try:

                    quantum = parse_int(

                        raw_quantum,

                        "Time quantum",

                        minimum=1

                    )

                except ValueError:

                    quantum = DEFAULT_QUANTUM

            # ------------------------------------------------
            # Read Process Information
            # ------------------------------------------------

            ids = request.form.getlist("pid")

            arrivals = request.form.getlist("arrival")

            bursts = request.form.getlist("burst")

            priorities = request.form.getlist("priority")

            # Check submitted data

            if not (

                len(ids) == len(arrivals) == len(bursts)

            ):

                raise ValueError(

                    "Process data is incomplete. "
                    "Please check all process fields."

                )

            if len(ids) < process_count:

                raise ValueError(

                    "Please provide information for all "
                    "selected processes."

                )

            # ------------------------------------------------
            # Process Input Data
            # ------------------------------------------------

            submitted = []

            for i in range(process_count):

                pid = ids[i].strip()

                if not pid:

                    raise ValueError(

                        f"Process ID in row {i + 1} "
                        "cannot be empty."

                    )

                arrival = parse_int(

                    arrivals[i],

                    f"Arrival time of {pid}",

                    minimum=0

                )

                burst = parse_int(

                    bursts[i],

                    f"Burst time of {pid}",

                    minimum=1

                )

                if (

                    i < len(priorities)

                    and priorities[i].strip()

                ):

                    priority = parse_int(

                        priorities[i],

                        f"Priority of {pid}",

                        minimum=1

                    )

                else:

                    priority = 1

                submitted.append({

                    "id": pid,

                    "arrival": arrival,

                    "burst": burst,

                    "priority": priority

                })

            # ------------------------------------------------
            # Check Duplicate IDs
            # ------------------------------------------------

            submitted_ids = [

                p["id"]

                for p in submitted

            ]

            if len(submitted_ids) != len(set(submitted_ids)):

                raise ValueError(

                    "Duplicate Process IDs are not allowed."

                )

            # Preserve submitted information

            process_values = submitted

            # ------------------------------------------------
            # EXECUTE SELECTED ALGORITHM
            # ------------------------------------------------

            selected = summarize_schedule(

                process_values,

                algorithm,

                quantum

            )

            results = selected["results"]

            gantt_chart = selected["gantt_chart"]

            avg_waiting = selected["avg_waiting"]

            avg_turnaround = selected["avg_turnaround"]

            avg_response = selected["avg_response"]

            utilization = selected["utilization"]

            throughput = selected["throughput"]

            idle_time = selected["idle_time"]

            makespan = selected["makespan"]

            calculated = True

            # ------------------------------------------------
            # COMPARE ALL ALGORITHMS
            # ------------------------------------------------

            if action == "compare":

                comparison_results = compare_algorithms(

                    process_values,

                    quantum

                )

                observations = generate_observations(

                    comparison_results

                )

                compared = True

        # ----------------------------------------------------
        # INPUT AND SCHEDULING ERRORS
        # ----------------------------------------------------

        except (ValueError, KeyError, TypeError) as exc:

            error = str(exc)

            calculated = False

            compared = False

            results = []

            gantt_chart = []

            comparison_results = []

            observations = []

        except Exception:

            app.logger.exception(

                "Unexpected scheduling application error."

            )

            error = (

                "An unexpected error occurred during "
                "the scheduling simulation. "
                "Please check the terminal."

            )

            calculated = False

            compared = False

    # --------------------------------------------------------
    # RENDER APPLICATION
    # --------------------------------------------------------

    return render_template(

        "index.html",

        # Process Configuration

        allowed_counts=ALLOWED_COUNTS,

        process_count=process_count,

        process_values=process_values,

        # Individual Scheduling Results

        results=results,

        gantt_chart=gantt_chart,

        # Performance Metrics

        avg_waiting=avg_waiting,

        avg_turnaround=avg_turnaround,

        avg_response=avg_response,

        utilization=utilization,

        throughput=throughput,

        idle_time=idle_time,

        makespan=makespan,

        # Comparison Results

        comparison_results=comparison_results,

        observations=observations,

        # Configuration

        algorithm=algorithm,

        quantum=quantum,

        # Application Status

        error=error,

        calculated=calculated,

        compared=compared

    )


# ============================================================
# 9. HEALTH CHECK ROUTE
# ============================================================

@app.route("/health", methods=["GET"])
def health():

    return {

        "status": "running",

        "application": "CPU Scheduling Visualizer",

        "algorithms": ALGORITHMS,

        "version": "2.0"

    }


# ============================================================
# 10. APPLICATION ENTRY POINT
# ============================================================

URL = "http://127.0.0.1:5000/"

EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def open_browser():
    """Open the app in Microsoft Edge, or the default browser if Edge is not found."""
    for path in EDGE_PATHS:
        if os.path.exists(path):
            subprocess.Popen([path, URL])
            return
    webbrowser.open_new(URL)


if __name__ == "__main__":

    debug_mode = os.environ.get("FLASK_DEBUG") == "1"

    # With debug on, Flask's reloader starts this script twice.
    # Only open the browser in the process that actually serves the app.
    if not debug_mode or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        opener = threading.Timer(1.0, open_browser)
        opener.daemon = True
        opener.start()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=debug_mode
    )