# Green Lab Group 1

### Setup
#### 1. Run this git command to pull EnergiBridge and experiment-runner.

```bash
git submodule update --init
```

#### 2. Follow the install instructions for EnergiBridge and Experiement Runner

#### 3. Run this command to collect the Run Table
```bash
python experiment-runner/experiment-runner/ ./Experiments/RunnerConfig.py
```

### The Run Table is under the directory:
```
Experiments/experiments/GreenLab_Compiler_Experiment{timestamp.now()}
```
