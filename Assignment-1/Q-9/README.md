# Q9 - Threaded Job Scheduler Simulation

## Problem
Simulate a job scheduler with multiple workers.

Each job contains:
- Arrival time
- Job ID
- Priority
- Duration
- Required resources

Higher priority jobs are processed first.
Jobs having the same priority are processed according to earlier
arrival order.

## File
12402080601054_Assignment1_Q9.py

## Requirements
- Python 3.10 or above
- No external libraries required

## Input Format

First line:
w n

Next n lines:
arrival_time job_id priority duration resources

## Output Format

job_id worker_id start_time finish_time

Finally:
AVG_WAIT average_waiting_time

## Example

Input:

2 3
0 J1 2 5 1
1 J2 5 3 1
2 J3 2 2 1

Output:

J1 W1 0 5
J2 W2 1 4
J3 W2 4 6
AVG_WAIT 0.67

## Data Structures Used

1. Priority Queue
   - Stores waiting jobs.
   - Higher priority jobs are selected first.

2. Min Heap
   - Stores workers according to their next available time.

3. List
   - Stores all jobs and final execution results.

## Algorithm

1. Read all jobs.
2. Sort jobs by arrival time.
3. Create a min-heap containing all workers.
4. Add arrived jobs to the waiting priority queue.
5. Select the highest-priority waiting job.
6. Select the earliest available worker.
7. Calculate start and finish time.
8. Update worker availability.
9. Continue until all jobs are completed.
10. Calculate average waiting time.

## Complexity

Time Complexity:
O(n log n)

Space Complexity:
O(n + w)

## Test Cases

Test the program using:
- Normal input
- Single worker
- Multiple workers
- Same priority jobs
- Same arrival time
- Jobs arriving at different times
- Highest-priority waiting jobs
- Boundary values

## Run Command

python 12402080601054_Assignment1_Q9.py
