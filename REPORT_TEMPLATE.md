# CPU Scheduling Visualizer — Demonstration Report

> Complete the bracketed fields with your real lab details. Insert your own screenshots and observations from running the project. Do not report results you did not observe.

## 1. Group and project details

| Field | Details |
|---|---|
| Subject / course code | Operating System — 25PCOS201 |
| Project title | CPU Scheduling Studio: OS Visualization & Simulation |
| Faculty | Prof. Puja Das |
| Group members and USNs | [List each member and USN] |
| Date of demonstration | [Date] |
| Python version / OS / browser | [Record environment] |

## 2. Aim and scope

The project visualizes how four CPU scheduling policies assign a single CPU to processes with arrival times and CPU burst lengths. It calculates per-process completion, turnaround, waiting, and response times, and displays a Gantt chart and summary statistics. The policies are FCFS, non-preemptive SJF, non-preemptive Priority (smaller value means higher priority), and Round Robin (configurable time quantum).

## 3. Reproducible procedure

1. Create and activate a Python virtual environment, then install packages with `python -m pip install -r requirements.txt`.
2. Start the application using `python app.py` and open `http://127.0.0.1:5000`.
3. Enter the workload below. Use unique process IDs, non-negative integer arrival times, positive integer bursts/priorities, and record the Round Robin quantum.
4. Select **Compare all policies**. This runs all four methods on the same inputs; retain the comparison table and Gantt chart in the evidence section.
5. Repeat with a second workload (for example, staggered arrivals or a long job followed by short jobs) to observe how workload shape changes the comparison.

### Workload A

| Process | Arrival | Burst | Priority |
|---|---:|---:|---:|
| P1 | [ ] | [ ] | [ ] |
| P2 | [ ] | [ ] | [ ] |
| P3 | [ ] | [ ] | [ ] |
| Additional processes | [Add rows as used] | | |

Round Robin quantum: **[ ]**

### Workload B

| Process | Arrival | Burst | Priority |
|---|---:|---:|---:|
| P1 | [ ] | [ ] | [ ] |
| P2 | [ ] | [ ] | [ ] |
| P3 | [ ] | [ ] | [ ] |
| Additional processes | [Add rows as used] | | |

Round Robin quantum: **[ ]**

## 4. Observations and data analysis

Attach a screenshot of each run. Transcribe the values shown by the app and explain at least one row by hand:

- Turnaround time = completion time − arrival time.
- Waiting time = turnaround time − burst time.
- Response time = first CPU start − arrival time.
- CPU utilization = total busy CPU time ÷ elapsed time from time zero to the final completion × 100%.

**Observed result for [workload]:** [State the measured averages and identify what the Gantt chart shows.]

**Hand calculation for process [ID]:** Arrival [ ], Burst [ ], First start [ ], Completion [ ], therefore turnaround [ ] and waiting [ ]. Explain why this agrees with the execution trace.

**Interpretation:** [Discuss how arrivals, burst lengths, priorities, and quantum explain the observed results. Mention any idle interval or preemption visible in the trace.]

## 5. Comparative analysis

Copy the app's comparison table for each workload and discuss the measured trade-offs:

| Policy | Avg waiting | Avg turnaround | Avg response | CPU utilization | Makespan |
|---|---:|---:|---:|---:|---:|
| FCFS | | | | | |
| SJF | | | | | |
| Priority | | | | | |
| Round Robin (q = [ ]) | | | | | |

**Evidence-based conclusion:** [For this workload, identify the policy with the lowest waiting time and the policy with the best response time. Use values from the table. Explain why a different workload or quantum could change the conclusion; avoid claiming that one policy is universally best.]

## 6. Implementation notes and limitations

The simulator uses one CPU and integer time units. FCFS, SJF, and Priority are non-preemptive; Round Robin is preemptive. Lower priority numbers represent higher priority. Arrival ties follow input order where applicable. This educational model does not include context-switch overhead, I/O bursts, multiple cores, or priority aging. These assumptions affect how closely results represent a production operating system.

## 7. Team contribution and technical discussion

| Member / USN | Work personally completed | Evidence / files or demo part |
|---|---|---|
| [Name / USN] | [Accurate contribution] | [ ] |
| [Name / USN] | [Accurate contribution] | [ ] |
| [Name / USN] | [Accurate contribution] | [ ] |
| [Name / USN] | [Accurate contribution] | [ ] |

Prepare each member to explain:

1. How the ready queue is selected for each policy, and which policies preempt.
2. How the Gantt chart supports a waiting-time calculation for one process.
3. Why Round Robin response/waiting behavior changes when the quantum changes.
4. One observed case where the policy with the lowest average waiting time is not necessarily the best choice for interactive response.
5. One limitation of the model and a technically reasonable improvement.

## 8. Evidence checklist

- [ ] App starts locally and accepts the stated configuration.
- [ ] Screenshots show process inputs, selected policy/quantum, Gantt trace, and result table.
- [ ] Comparison uses identical inputs for all policies.
- [ ] Report values match the displayed application output.
- [ ] Each group member's contribution is listed truthfully and each member can explain their work.
