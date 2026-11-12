# CPU Scheduling Studio

A small Flask app for entering processes, running common CPU scheduling policies, and comparing their Gantt charts and timing statistics.

Use **Run schedule** to inspect one policy or **Compare all policies** to run FCFS, SJF, Priority, and Round Robin on the same process data. The comparison includes average waiting, turnaround and response times, CPU utilization, and makespan. The process table includes first start and response time, and the Gantt chart shows idle intervals and Round Robin slices.

## Run locally

Requires Python 3.10 or newer.

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5000> in a browser. Stop the server with `Ctrl+C`.

## Policies

- **FCFS**: non-preemptive, ordered by arrival time; ties keep the input order.
- **SJF**: non-preemptive; chooses the shortest burst among processes that have arrived.
- **Priority**: non-preemptive; the lowest positive priority number wins. Ties use arrival time, then input order.
- **Round Robin**: preemptive, with a configurable positive integer quantum. Processes that arrive during a time slice join the ready queue before the running process is requeued.

The app reports completion time, turnaround time (`completion − arrival`), waiting time (`turnaround − burst`), average waiting and turnaround times, and CPU utilization. Idle gaps are included in the Gantt chart. All times use abstract integer units, and the model has one CPU.

## Project files

- `app.py` — Flask routes, form validation, and page rendering.
- `scheduler.py` — scheduling algorithms and timing calculations.
- `templates/index.html` — responsive interface, Gantt chart, and results table.
- `requirements.txt` — Python dependencies.
- `REPORT_TEMPLATE.md` — reproducible demonstration procedure, evidence checklist, analysis prompts, and team contribution record for the course rubric.

## Assessment evidence

The project supports simulation execution through configurable inputs and four policies; observation through a Gantt chart and per-process/aggregate metrics; and comparative analysis through the same-input policy comparison. Use `REPORT_TEMPLATE.md` to record your actual runs, screenshots, hand calculations, workload-based conclusions, environment, and individual contributions. The report prompts are not pre-filled with fabricated experiment results: complete them from your demonstration and be ready to explain your own work.

## Project Contributors

- Chandra Prakash – Developer
- Tuibaa ALtaf Bhat – Developer

## Team Members

This project was collaboratively developed by
[ChandraPrakash-1103](https://github.com/ChandraPrakash-1103)
and [Tuibaa-Bhat](https://github.com/Tuibaa-Bhat).