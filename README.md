# msc-thesis
Benchmarking feature rankers using [fseval](https://github.com/dunnkers/fseval) on [Peregrine](https://www.rug.nl/society-business/centre-for-information-technology/research/services/hpc/facilities/peregrine-hpc-cluster?lang=en).

<a href="https://docs.google.com/presentation/d/e/2PACX-1vRmOR0McIVtZOPiu2rI2NE2VN2cuFZ442BUjsBqhSn6QKEnRVlBaVtkzbOU25MLZQCXL17cCFoUl_mf/pub?start=false&loop=false&delayms=3000">
    <img width="965" alt="Screen Shot 2022-01-28 at 10 09 47" src="https://user-images.githubusercontent.com/744430/151518929-9f006db6-b09b-442c-b359-0b07c1664e69.png">
</a>


## Install
Install [fseval](https://github.com/dunnkers/fseval).

```shell
pip install fseval==2.1.2
```

## Enqueueing jobs
Enqueue jobs by running:

```shell
pg -t "srun --ntasks=1 --time=02:00:00 --mem=10000 --chdir=/scratch/s2995697/fseval/ --partition=regular --pty bash -i"

sh ~/msc-thesis/jobs/_prepare_env.sh
module load Python/3.8.6-GCCcore-10.2.0
source $TMPDIR/venv_${SLURM_JOB_ID}_${SLURM_ARRAY_TASK_ID}/bin/activate

fseval \
    "--multirun" \
    "+dataset=synclf_easy" \
    "+estimator@ranker=multisurf" \
    "+estimator@validator=decision_tree" \
    "resample=bootstrap" \
    "resample.sample_size=1.0" \
    "n_bootstraps=25" \
    "n_jobs=13" \
    "storage=local" \
    "callbacks=[wandb]" \
    "++callbacks.wandb.project=fseval" \
    "++callbacks.wandb.log_metrics=true" \
    "++callbacks.wandb.resume=allow" \
    "++callbacks.wandb.group=fixing-runs" \
    "hydra/launcher=rq" \
    "hydra.launcher.queue=fixing-runs" \
    "hydra.launcher.enqueue.result_ttl=1d" \
    "hydra.launcher.enqueue.failure_ttl=60d" \
    "hydra.launcher.stop_after_enqueue=true" \
    "hydra.launcher.fail_hard=true"
```

(see Peregrine [wiki page](https://github.com/dunnkers/msc-thesis/wiki/Peregrine#cli-aliases-and-shortcuts) for command-line aliases like `pg`)

⚠️ Mind carefully: when using the RQ launcher jobs **must** be launched in exactly the same environment as in which the jobs will eventually run: this has to do with how `cloudpickle` works: the serializer and deserializer of the jobs to- and from Redis.

## Running workers on Peregrine
> Make sure to set the `PEREGRINE_USERNAME` environment variable both locally and on the cluster.

From your laptop, run:

```shell
pg "cd msc-thesis; git pull && git log -n 1"
pg "sbatch --array=0-1 --ntasks=1 --dependency=afterok:20809105 --partition=regular --mem=20000 --time=24:00:00 --export=queue=add-mean-vali-score,burst=--burst ~/msc-thesis/jobs/rq_worker.sh"
```

## Enqueue runs
```shell
pg "cd msc-thesis; git pull && git log -n 1"
pg "sbatch ~/msc-thesis/jobs/enqueue_runs.sh"
pg "sbatch --array=0 --mem=54000 --ntasks=9 --partition=regular --time=24:00:00 --export=queue=fixing-runs,burst=--burst --job-name=fixing-runs ~/msc-thesis/jobs/rq_worker.sh"
```


## Running the RQ dashboard
```shell
rq-dashboard -u $REDIS_URL
```
## Built-ins
Several rankers, datasets and validators are already built-in.

<details>
<summary>Built-in Feature Rankers</summary>

| Ranker | Source | Command | Classif- ication | Regr- ession | Multi output | Feature importance | Feature support | Feature ranking |
|-|-|-|-|-|-|-|-|-|
| ANOVA F-value | [sklearn](https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.f_classif.html) | <details><summary>cli</summary>`+estimator@ranker=anova_f_value`</details>| ✓ | ✓ |  | ✓ |  |  |
| Boruta | [github](https://github.com/scikit-learn-contrib/boruta_py) <details><summary>install</summary>`pip install Boruta`</details> | <details><summary>cli</summary>`+estimator@ranker=boruta`</details>| ✓ |  |  |  | ✓ | ✓ |
| Chi-Squared | [sklearn](https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.chi2.html) | <details><summary>cli</summary>`+estimator@ranker=chi2`</details>| ✓ |  |  | ✓ |  |  |
| Decision Tree | [sklearn](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html) | <details><summary>cli</summary>`+estimator@ranker=decision_tree`</details>| ✓ | ✓ | ✓ | ✓ |  |  |
| FeatBoost | [github](https://github.com/amjams/FeatBoost) <details><summary>install</summary>`pip install git+https://github.com/amjams/FeatBoost.git`</details> | <details><summary>cli</summary>`+estimator@ranker=featboost`</details>| ✓ |  |  | ✓ | ✓ |  |
| Infinite Selection | [github](https://github.com/giorgioroffo/Infinite-Feature-Selection) <details><summary>install</summary>`pip install git+https://github.com/dunnkers/infinite-selection.git` ℹ️</details> | <details><summary>cli</summary>`+estimator@ranker=infinite_selection`</details>| ✓ |  |  | ✓ |  | ✓ |
| MultiSURF | [github](https://github.com/EpistasisLab/scikit-rebate) <details><summary>install</summary>`pip install skrebate`</details> | <details><summary>cli</summary>`+estimator@ranker=multisurf`</details>| ✓ | ✓ |  | ✓ |  |  |
| Mutual Info | [github](https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.mutual_info_classif.html) | <details><summary>cli</summary>`+estimator@ranker=mutual_info`</details>| ✓ | ✓ |  | ✓ |  |  |
| ReliefF | [github](https://github.com/EpistasisLab/scikit-rebate) <details><summary>install</summary>`pip install skrebate`</details> | <details><summary>cli</summary>`+estimator@ranker=relieff`</details>| ✓ | ✓ |  | ✓ |  |  |
| Stability Selection | [github](https://github.com/scikit-learn-contrib/stability-selection) <details><summary>install</summary>`pip install git+https://github.com/dunnkers/stability-selection.git matplotlib` ℹ️</details> | <details><summary>cli</summary>`+estimator@ranker=stability_selection`</details>| ✓ |  |  | ✓ | ✓ |  |
| TabNet | [github](https://github.com/dreamquark-ai/tabnet) <details><summary>install</summary>`pip install pytorch-tabnet`</details> | <details><summary>cli</summary>`+estimator@ranker=tabnet`</details>| ✓ | ✓ | ✓ | ✓ |  |  |
| XGBoost | [github](https://xgboost.readthedocs.io/) <details><summary>install</summary>`pip install xgboost`</details> | <details><summary>cli</summary>`+estimator@ranker=xgb`</details>| ✓ | ✓ |  | ✓ |  |  |

ℹ️ This library was customized to make it compatible with the fseval pipeline.

If you would like to install simply all dependencies, download the fseval [requirements.txt](https://github.com/dunnkers/fseval/blob/master/requirements.txt) file and run `pip install -r requirements.txt`.

</details>

<details>
<summary>Built-in Datasets</summary>

| Dataset                       | Source | Command | `n` | `p` | Task   | Multi- output | Domain                       | 
|-------------------------------------------|-------|-------------|-------------|----------------|------------------------|--------------------------------------|----------------------------------------|
| Boston house prices      | [OpenML](https://www.openml.org/d/531) <details><summary>install</summary>`pip install openml`</details>                                      | <details><summary>cli</summary>`+dataset=boston`</details> | 506         | 11          | Regression     | No                     | Finance                              |
| Additive (Chen et al. [L2X](https://github.com/Jianbo-Lab/L2X))                                 | [Synthetic](https://github.com/dunnkers/l2x_synthetic) <details><summary>install</summary>`pip install l2x-synthetic`</details> | <details><summary>cli</summary>`+dataset=chen_additive`</details> | 10000       | 10          | Regression     | Yes                    | Synthetic                            |
| Orange (Chen et al. [L2X](https://github.com/Jianbo-Lab/L2X))                                   | [Synthetic](https://github.com/dunnkers/l2x_synthetic) <details><summary>install</summary>`pip install l2x-synthetic`</details> | <details><summary>cli</summary>`+dataset=chen_orange`</details> | 10000       | 10          | Regression     | Yes                    | Synthetic                            |
| XOR (Chen et al. [L2X](https://github.com/Jianbo-Lab/L2X))                                      | [Synthetic](https://github.com/dunnkers/l2x_synthetic) <details><summary>install</summary>`pip install l2x-synthetic`</details> | <details><summary>cli</summary>`+dataset=chen_xor`</details> | 10000       | 10          | Regression     | Yes                    | Synthetic                            |
| Climate Model Simulation         | [OpenML](https://www.openml.org/d/40994) ([CC18](https://docs.openml.org/benchmark/#openml-cc18)) <details><summary>install</summary>`pip install openml`</details> | <details><summary>cli</summary>`+dataset=climate_model_simulation`</details> | 540 | 18          | Classification | No                     | Nature                               | 
| Cylinder bands                            | [OpenML](https://www.openml.org/d/1497) ([CC18](https://docs.openml.org/benchmark/#openml-cc18)) <details><summary>install</summary>`pip install openml`</details> | <details><summary>cli</summary>`+dataset=cylinder_bands`</details> | 5456        | 24          | Classification | No                     | Mechanics                            | 
| Iris Flowers                              | [OpenML](https://www.openml.org/d/61) <details><summary>install</summary>`pip install openml`</details>                                      | <details><summary>cli</summary>`+dataset=iris`</details> | 150         | 4           | Classification | No                     | Nature                               | 
| Madelon                                   | [OpenML](https://www.openml.org/d/1485) <details><summary>install</summary>`pip install openml`</details> | <details><summary>cli</summary>`+dataset=madelon`</details> | 2600        | 500         | Classification | No                     | Synthetic                            | 
| Multifeat Pixel                           | [OpenML](https://www.openml.org/d/40979) ([CC18](https://docs.openml.org/benchmark/#openml-cc18)) <details><summary>install</summary>`pip install openml`</details> | <details><summary>cli</summary>`+dataset=mfeat_pixel`</details> | 2000        | 240         | Classification | No                     | OCR                                  | 
| Nomao                                     | [OpenML](https://www.openml.org/d/1486) ([CC18](https://docs.openml.org/benchmark/#openml-cc18)) <details><summary>install</summary>`pip install openml`</details> | <details><summary>cli</summary>`+dataset=nomao`</details> | 34465       | 89          | Classification | No                     | Geodata                              | 
| Ozone Levels                              | [OpenML](https://www.openml.org/d/1487) ([CC18](https://docs.openml.org/benchmark/#openml-cc18)) <details><summary>install</summary>`pip install openml`</details> | <details><summary>cli</summary>`+dataset=ozone_levels`</details> | 2534        | 72          | Classification | No                     | Nature                               | 
| Phoneme                                   | [OpenML](https://www.openml.org/d/1489) ([CC18](https://docs.openml.org/benchmark/#openml-cc18)) <details><summary>install</summary>`pip install openml`</details> | <details><summary>cli</summary>`+dataset=phoneme`</details> | 5404        | 5           | Classification | No                     | Biomedical                           | 
| Synclf easy                               | [Synthetic](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_classification.html)                               | <details><summary>cli</summary>`+dataset=synclf_easy`</details> | 10000       | 20          | Classification | No                     | Synthetic                            | 
| Synclf medium                             | [Synthetic](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_classification.html)                               | <details><summary>cli</summary>`+dataset=synclf_medium`</details> | 10000       | 30          | Classification | No                     | Synthetic                            | 
| Synclf hard                               | [Synthetic](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_classification.html)                               | <details><summary>cli</summary>`+dataset=synclf_hard`</details> | 10000       | 50          | Classification | No                     | Synthetic                            | 
| Synclf very hard                          | [Synthetic](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_classification.html)                               | <details><summary>cli</summary>`+dataset=synclf_very_hard`</details> | 10000       | 50          | Classification | No                     | Synthetic                            | 
| Synreg easy                               | [Synthetic](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_regression.html) | <details><summary>cli</summary>`+dataset=synreg_easy`</details> | 10000       | 10          | Regression     | No                     | Synthetic                            |
| Synreg medium                             | [Synthetic](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_regression.html) | <details><summary>cli</summary>`+dataset=synreg_medium`</details> | 10000       | 10          | Regression     | No                     | Synthetic                            |
| Synreg hard                               | [Synthetic](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_regression.html) | <details><summary>cli</summary>`+dataset=synreg_hard`</details> | 10000       | 20          | Regression     | No                     | Synthetic                            |
| Synreg hard                               | [Synthetic](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_regression.html) | <details><summary>cli</summary>`+dataset=synreg_very_hard`</details> | 10000       | 20          | Regression     | No                     | Synthetic                            |
| Texture                                   | [OpenML](https://www.openml.org/d/40499) ([CC18](https://docs.openml.org/benchmark/#openml-cc18)) <details><summary>install</summary>`pip install openml`</details> | <details><summary>cli</summary>`+dataset=texture`</details> | 5500        | 40          | Classification | No                     | Pattern Recognition | 
| Wall Robot Navigation    | [OpenML](https://www.openml.org/d/1497) ([CC18](https://docs.openml.org/benchmark/#openml-cc18)) <details><summary>install</summary>`pip install openml`</details> | <details><summary>cli</summary>`+dataset=wall_robot_navigation`</details> | 5456        | 24          | Classification | No                     | Mechanics                            | 

- `n`: number of dataset **samples**.
- `p`: number of dataset **dimensions**.
</details>

<details>
<summary>Built-in Validators</summary>

| Validator | Source | Command | Classification | Regression | Multioutput |
|-|-|-|-|-|-|
| Decision Tree | [sklearn](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html) | <details><summary>cli</summary>`+estimator@validator=decision_tree`</details>| ✓ | ✓ | ✓ |
| k-NN | [sklearn](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html) | <details><summary>cli</summary>`+estimator@validator=knn`</details>| ✓ |   |   |
| TabNet | [github](https://github.com/dreamquark-ai/tabnet) <details><summary>install</summary>`pip install pytorch-tabnet`</details> | <details><summary>cli</summary>`+estimator@validator=tabnet`</details>| ✓ | ✓ | ✓ |
| XGBoost | [github](https://xgboost.readthedocs.io/) <details><summary>install</summary>`pip install xgboost`</details> | <details><summary>cli</summary>`+estimator@validator=xgb`</details>| ✓ | ✓ |  |

</details>


ℹ️ Note you *cannot* mix built-ins and custom rankers/datasets/validators in a **multirun**. This is due to the behavior of the [Hydra](https://github.com/facebookresearch/hydra) library.


## fseval
The project assumes fseval version [v2.1.2](https://github.com/dunnkers/fseval/releases/tag/v2.1.2) is used.
