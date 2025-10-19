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


class RunnerConfig:
    ROOT_DIR = Path(dirname(realpath(__file__)))

    name: str = "GreenLab_Compiler_Experiment" + str(time.time)
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
        self.profiler = None
        self.target = None
        output.console_log("Custom config loaded")

    def create_run_table_model(self) -> RunTableModel:
        compiler_factor = FactorModel("compiler", ["pure_python", "cython", "swig"])
        self.run_table_model = RunTableModel(
            factors=[compiler_factor],
            data_columns=[
                "execution_time (s)",
                "cpu_usage (%)",
                "memory_usage (MB)",
                "energy_consumption (J)"
            ],
            shuffle=True,
            repetation=5
        )
        return self.run_table_model

    def before_experiment(self) -> None:
        output.console_log("Config.before_experiment() called!")
        os.makedirs(self.results_output_path, exist_ok=True)

    def before_run(self) -> None:
        output.console_log("Config.before_run() called!")

    def start_run(self, context: RunnerContext) -> None:
        compiler = context.run_variation["compiler"]
        target_dir = self.ROOT_DIR / compiler
        target_script = target_dir / "main.py"

        if not target_script.exists():
            raise FileNotFoundError(f"Target script not found: {target_script}")

        output.console_log(f"Starting run for compiler: {compiler}")

        cmd = f"python {target_script}"
        self.target = subprocess.Popen(
            shlex.split(cmd),
            cwd=target_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

    def start_measurement(self, context: RunnerContext) -> None:
        output.console_log("Config.start_measurement() called!")
        compiler = context.run_variation["compiler"]
        profiler_cmd = f"energibridge --output {context.run_dir / 'energibridge.csv'} --summary python experiments/runner/{compiler}.py"
        self.profiler = subprocess.Popen(shlex.split(profiler_cmd))
        time.sleep(0.5)

    def interact(self, context: RunnerContext) -> None:
        output.console_log("Config.interact() called - waiting for target process.")
        if self.target:
            self.target.wait()

    def stop_measurement(self, context: RunnerContext) -> None:
        output.console_log("Config.stop_measurement() called!")
        if self.profiler:
            try:
                self.profiler.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.profiler.terminate()

    def stop_run(self, context: RunnerContext) -> None:
        output.console_log("Config.stop_run() called!")
        if self.target and self.target.poll() is None:
            self.target.terminate()

    def populate_run_data(self, context: RunnerContext) -> Optional[Dict[str, Any]]:
        csv_path = context.run_dir / "energibridge.csv"

        if not csv_path.exists():
            output.console_log(f"No measurement file found at {csv_path}")
            return None

        df = pd.read_csv(csv_path)

        cpu_cols = [c for c in df.columns if "CPU_USAGE" in c]
        avg_cpu = df[cpu_cols].mean().mean() if cpu_cols else 0

        run_data = {
            "execution_time (s)": round((df["Time"].iloc[-1] - df["Time"].iloc[0]) / 1000, 3),
            "cpu_usage (%)": round(avg_cpu, 3),
            "memory_usage (MB)": round(df["USED_MEMORY"].mean() / 1024, 3),
            "energy_consumption (J)": round(df["SYSTEM_POWER (Watts)"].mean(), 3),
        }

        return run_data

    def after_experiment(self) -> None:
        output.console_log("Config.after_experiment() called!")

    experiment_path: Path = None


def run_experiment(config: RunnerConfig):
    output.console_log(f"Starting experiment: {config.name}")

    config.experiment_path = config.results_output_path / config.name
    os.makedirs(config.experiment_path, exist_ok=True)

    EventSubscriptionController.publish(RunnerEvents.BEFORE_EXPERIMENT)

    run_table = config.create_run_table_model()
    runs = run_table.generate_runs()

    output.console_log(f"Total runs to perform: {len(runs)}")

    for idx, run_variation in enumerate(runs, start=1):
        output.console_log(f"Starting Run {idx}/{len(runs)}: {run_variation}")

        run_dir = config.experiment_path / f"run_{idx:03d}"
        os.makedirs(run_dir, exist_ok=True)

        context = RunnerContext(
            run_index=idx,
            run_dir=run_dir,
            run_variation=run_variation,
            operation_type=config.operation_type
        )

        try:
            EventSubscriptionController.publish(RunnerEvents.BEFORE_RUN)
            EventSubscriptionController.publish(RunnerEvents.START_RUN, context)
            EventSubscriptionController.publish(RunnerEvents.START_MEASUREMENT, context)
            EventSubscriptionController.publish(RunnerEvents.INTERACT, context)
            EventSubscriptionController.publish(RunnerEvents.STOP_MEASUREMENT, context)
            EventSubscriptionController.publish(RunnerEvents.STOP_RUN, context)

            run_data = EventSubscriptionController.publish(RunnerEvents.POPULATE_RUN_DATA, context)
            if isinstance(run_data, dict):
                run_table.add_result(run_variation, run_data)
        except Exception as e:
            output.console_log(f"Error during run {idx}: {e}")
        finally:
            output.console_log(f"Waiting {config.time_between_runs_in_ms} ms before next run...")
            time.sleep(config.time_between_runs_in_ms / 1000.0)

    EventSubscriptionController.publish(RunnerEvents.AFTER_EXPERIMENT)

    result_file = config.experiment_path / "final_results.csv"
    run_table.save_to_csv(result_file)
    output.console_log(f"Experiment complete. Results saved to: {result_file}")


if __name__ == "__main__":
    cfg = RunnerConfig()
    run_experiment(cfg)
