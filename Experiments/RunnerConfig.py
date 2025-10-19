from EventManager.Models.RunnerEvents import RunnerEvents
from EventManager.EventSubscriptionController import EventSubscriptionController
from ConfigValidator.Config.Models.RunTableModel import RunTableModel
from ConfigValidator.Config.Models.FactorModel import FactorModel
from ConfigValidator.Config.Models.RunnerContext import RunnerContext
from ConfigValidator.Config.Models.OperationType import OperationType
from ProgressManager.Output.OutputProcedure import OutputProcedure as output

from typing import Dict, Any, Optional
from pathlib import Path
from os.path import dirname, realpath

import os
import subprocess
import shlex
import pandas as pd
import time
import datetime


class RunnerConfig:
    ROOT_DIR = Path(dirname(realpath(__file__)))

    name: str = "GreenLab_Compiler_Experiment" + str(datetime.datetime.now().timestamp())
    results_output_path: Path = ROOT_DIR / "experiments"
    operation_type: OperationType = OperationType.AUTO
    time_between_runs_in_ms: int = 1000

    def __init__(self):
        EventSubscriptionController.subscribe_to_multiple_events([
            (RunnerEvents.BEFORE_EXPERIMENT, self.before_experiment),
            (RunnerEvents.BEFORE_RUN, self.before_run),
            (RunnerEvents.START_RUN, self.start_run),
            (RunnerEvents.START_MEASUREMENT, self.start_measurement),
            (RunnerEvents.INTERACT, self.interact),
            (RunnerEvents.STOP_MEASUREMENT, self.stop_measurement),
            (RunnerEvents.STOP_RUN, self.stop_run),
            (RunnerEvents.POPULATE_RUN_DATA, self.populate_run_data),
            (RunnerEvents.AFTER_EXPERIMENT, self.after_experiment),
        ])
        self.run_table_model = None
        output.console_log("Custom config loaded")

    def create_run_table_model(self) -> RunTableModel:
        compiler_factor = FactorModel("_compiler", ["pure_python", "cython", "swig"])
        benchmark_factor = FactorModel("_benchmark", ["bfs", "convex", "dense_matrix", "fft", "json_bench", "k_means", "quick_sort", "regex", "sieve", "nbody"])
        self.run_table_model = RunTableModel(
            factors=[compiler_factor, benchmark_factor],
            data_columns=[
                "execution_time (s)",
                "cpu_usage (%)",
                "memory_usage (MB)",
                "energy_consumption (J)"
            ],
            shuffle=True,
            repetitions=20
        )
        return self.run_table_model

    def before_experiment(self) -> None:
        output.console_log("Config.before_experiment() called!")
        os.makedirs(self.results_output_path, exist_ok=True)

    def before_run(self) -> None:
        output.console_log("Config.before_run() called!")

    def start_run(self, context: RunnerContext) -> None:
        pass

    def start_measurement(self, context: RunnerContext) -> None:
        output.console_log("Config.start_measurement() called!")
        compiler = context.execute_run["_compiler"]
        benchmark = context.execute_run["_benchmark"]

        ROOT_DIR = Path(dirname(realpath(__file__)))
        # output.console_log(compiler)

        if compiler == "pure_python":
            benchmark_file = f"{benchmark}.py"
        else:
            benchmark_file = f"{benchmark}/main.py"

        profiler_cmd = f"{ROOT_DIR}/energibridge --output {context.run_dir / 'energibridge.csv'} --summary python3 {ROOT_DIR}/runner/{compiler}/{benchmark_file}"

        output.console_log(profiler_cmd)
        self.profiler = subprocess.Popen(shlex.split(profiler_cmd))

    def interact(self, context: RunnerContext) -> None:
        pass

    def stop_measurement(self, context: RunnerContext) -> None:
        output.console_log("Config.stop_measurement() called!")
        if self.profiler:
            try:
                self.profiler.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.profiler.terminate()

    def stop_run(self, context: RunnerContext) -> None:
        output.console_log("Config.stop_run() called!")

    def populate_run_data(self, context: RunnerContext) -> Optional[Dict[str, Any]]:
        csv_path = context.run_dir / "energibridge.csv"

        if not csv_path.exists():
            output.console_log(f"No measurement file found at {csv_path}")
            return None

        df = pd.read_csv(csv_path)

        cpu_cols = [c for c in df.columns if "CPU_USAGE" in c]
        avg_cpu = df[cpu_cols].mean().mean() if cpu_cols else 0

        # Use CPU_ENERGY (J) instead of SYSTEM_POWER (Watts)
        energy_col = "CPU_ENERGY (J)" if "CPU_ENERGY (J)" in df.columns else None
        energy_val = round(df[energy_col].iloc[-1] - df[energy_col].iloc[0], 3) if energy_col else 0

        run_data = {
            "execution_time (s)": round((df["Time"].iloc[-1] - df["Time"].iloc[0]) / 1000, 3),
            "cpu_usage (%)": round(avg_cpu, 3),
            "memory_usage (MB)": round(df["USED_MEMORY"].mean() / 1024, 3),
            "energy_consumption (J)": energy_val,
        }

        return run_data

    def after_experiment(self) -> None:
        output.console_log("Config.after_experiment() called!")

    # ================================ DO NOT ALTER BELOW THIS LINE ================================
    experiment_path:            Path             = None