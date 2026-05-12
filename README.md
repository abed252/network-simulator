# network-simulator

A multi-server queueing system simulator written in Python.

Models **M/M/c queues with probabilistic routing**: inter-arrival times and service times are exponentially distributed (Poisson arrivals, exponential service). Incoming tasks are routed to one of *n* servers by a probability vector and dropped if the target queue is at capacity.

## Queueing model

```
Arrivals (rate λ, exponential inter-arrival)
         │
         ▼
     ┌────────┐
     │ Router │  probabilistic routing (p₁ … pₙ, Σpᵢ = 1)
     └────────┘
      /   |   \
     ▼    ▼    ▼
  [S₁] [S₂] [Sₙ]   capacity Kᵢ, service rate μᵢ (exponential)
```

- Arrival is routed to server *i* with probability *pᵢ*
- If that server's queue is full, the task is **rejected** (finite-buffer loss)
- Service times are independent exponential per server

## Usage

```bash
python3 main.py <T> <n> <p1> ... <pn> <λ> <K1> ... <Kn> <μ1> ... <μn>
```

| Parameter | Description |
|---|---|
| `T` | Simulation duration |
| `n` | Number of servers |
| `p1..pn` | Routing probabilities (must sum to 1.0) |
| `λ` | Global arrival rate |
| `K1..Kn` | Queue capacity per server |
| `μ1..μn` | Service rate per server |

### Example

Two servers, 60/40 routing split, arrival rate 5.0, capacity 10 each, service rates 3.0 and 4.0:

```bash
python3 main.py 1000 2 0.6 0.4 5.0 10 10 3.0 4.0
```

Output (space-separated):

```
<accepted> <rejected> <sim_end_time> <avg_wait_time> <avg_service_time>
```

## Output metrics

| Field | Description |
|---|---|
| `accepted` | Tasks admitted to a server queue |
| `rejected` | Tasks dropped due to full queue |
| `sim_end_time` | Time when the last queued task completes |
| `avg_wait_time` | Mean time a task waits before service begins |
| `avg_service_time` | Mean service duration |

## Requirements

- Python 3.x

## License

MIT
