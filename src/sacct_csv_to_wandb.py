import re
import sys
from io import StringIO

import humanfriendly
import pandas as pd
import wandb


def parse_duration_string(duration_str):
    if not duration_str:
        return duration_str

    match = re.match(r"(?:(\d*)-)?((?:\d\d:)?\d\d:\d\d)(?:.(\d*))?", duration_str)
    assert match is not None, f"incorrect duration format: {duration_str}"

    days, hhmmss, ms = match.groups()
    if not re.match(r"\d\d:\d\d:\d\d", hhmmss):
        hhmmss = f"00:{hhmmss}"

    days_duration = pd.to_timedelta(f"{days} days" if days else 0)
    hhmmss_duration = pd.to_timedelta(hhmmss)
    ms_duration = pd.to_timedelta(f"{ms} microseconds" if ms else 0)

    duration = days_duration + hhmmss_duration + ms_duration
    duration_seconds = duration.total_seconds()
    return duration_seconds


def parse_duration(series):
    return series.dropna().apply(parse_duration_string)


def parse_memory_string(memory_str):
    if not memory_str:
        return memory_str

    return humanfriendly.parse_size(memory_str) / 1e6


def parse_memory(series):
    return series.dropna().apply(parse_memory_string)


def construct_df(csv_input):
    # read csv to data frame
    df = pd.read_csv(
        csv_input, sep=";", parse_dates=["Eligible", "End", "Start", "Submit"]
    )

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

    # exit code
    parse_exit_code = lambda exit_code_str: int(exit_code_str.split(":")[1])
    df["ExitCode"] = df["ExitCode"].dropna().apply(parse_exit_code)

    return df


if __name__ == "__main__":
    # read input from stdin
    csv_input = ""
    for line in sys.stdin:
        csv_input += f"{line}\n"
    assert len(csv_input) > 0, "no sacct csv input"
    csv_input = StringIO(csv_input)

    # construct df
    print("constructing pandas dataframe...")
    df = construct_df(csv_input)
    print("dataframe constructed ✓")

    # upload to wandb
    for index, result in df.iterrows():
        wandb.init(
            project="peregrine",
            config=result.to_dict(),
            id=result["JobID"],
            job_type=result["JobName"],
            name=result["JobID"],
            tags=[result["State"]],
        )
        wandb.finish(exit_code=result["ExitCode"])
