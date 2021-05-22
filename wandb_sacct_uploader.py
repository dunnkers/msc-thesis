import humanfriendly
import pandas as pd

import wandb

df = pd.read_csv(
    "./logs/sacct.csv", sep=";", parse_dates=["Eligible", "End", "Start", "Submit"]
)


def parse_duration_string(duration_str):
    # convert `00:23.254` to `00:23`
    duration_str = duration_str.split(".")[0]

    # convert `00:23` to `00:00:23` to match "hh:mm:ss" format.
    duration_str = f"00:{duration_str}" if len(duration_str) == 5 else duration_str
    assert len(duration_str) == 8, f"incorrect duration format: {duration_str}"

    duration = pd.to_timedelta(duration_str)
    duration = duration.total_seconds()

    return humanfriendly.format_timespan(duration)


def parse_duration(series):
    return series.dropna().apply(parse_duration_string)


def parse_memory_string(memory_str):
    return humanfriendly.format_size(humanfriendly.parse_size(memory_str))


def parse_memory(series):
    return series.dropna().apply(parse_memory_string)


# parse durations
df["Elapsed"] = parse_duration(df["Elapsed"])
df["AveCPU"] = parse_duration(df["AveCPU"])
df["MinCPU"] = parse_duration(df["MinCPU"])
df["UserCPU"] = parse_duration(df["UserCPU"])
df["CPUTime"] = parse_duration(df["CPUTime"])
df["SystemCPU"] = parse_duration(df["SystemCPU"])
df["TotalCPU"] = parse_duration(df["TotalCPU"])
df["Timelimit"] = parse_duration(df["Timelimit"])
df["Suspended"] = parse_duration(df["Suspended"])

# parse memory storage: from any amount to Megabytes
df["AveCPUFreq"] = parse_memory(df["AveCPUFreq"])
df["AveDiskRead"] = parse_memory(df["AveDiskRead"])
df["AveDiskWrite"] = parse_memory(df["AveDiskWrite"])
df["AveRSS"] = parse_memory(df["AveRSS"])
df["AveVMSize"] = parse_memory(df["AveVMSize"])
df["MaxDiskRead"] = parse_memory(df["MaxDiskRead"])
df["MaxDiskWrite"] = parse_memory(df["MaxDiskWrite"])
df["MaxRSS"] = parse_memory(df["MaxRSS"])
df["MaxVMSize"] = parse_memory(df["MaxVMSize"])
df["ReqMem"] = parse_memory(df["ReqMem"])

for index, result in df.iterrows():
    wandb.init(
        project="msc-thesis",
        config=result.to_dict(),
        id=result["JobID"],
        job_type=result["JobName"],
        name=result["JobID"],
        tags=[result["State"]],
    )
    exit_code = int(result["ExitCode"].split(":")[1])
    wandb.finish(exit_code=exit_code)
