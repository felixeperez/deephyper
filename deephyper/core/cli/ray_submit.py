"""
Example Usage:
deephyper ray-submit nas regevo -w combo_test -n 1 -t 30 -A datascience -q full-node --problem nas_big_data.combo.problem.Problem --run deephyper.nas.run.alpha.run --max-evals 8 --num-cpus-per-task 1 --num-gpus-per-task 1 -as myscript.sh
"""
import os
import sys
from jinja2 import Template
from deephyper.search.util import generic_loader, banner
from deephyper.problem.neuralarchitecture import Problem
from deephyper.problem import BaseProblem

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))


def add_subparser(subparsers):
    subparser_name = "ray-submit"
    function_to_call = main

    subparser = subparsers.add_parser(
        subparser_name, help="Create and submit an HPS or NAS job directly via Balsam."
    )

    subparser.add_argument("mode", choices=["nas", "hps"], help="Type of search")
    subparser.add_argument(
        "search", choices=["ambs", "regevo", "random", "agebo"], help="Search strategy"
    )
    subparser.add_argument("-w", "--workflow", required=True, help="Unique workflow name")
    subparser.add_argument(
        "-p", "--problem", required=True, help="Problem definition path or object"
    )
    subparser.add_argument(
        "-r", "--run", required=True, help="Run function path or object"
    )

    subparser.add_argument(
        "-t", "--time-minutes", type=int, required=True, help="Job walltime (minutes)"
    )
    subparser.add_argument(
        "-n", "--nodes", type=int, required=True, help="Number of nodes"
    )
    subparser.add_argument("-q", "--queue", required=True, help="Queue to submit into")
    subparser.add_argument("-A", "--project", required=True, help="Project Name")
    subparser.add_argument(
        "-as",
        "--activation-script",
        required=True,
        help="Script to activate current conda environment.",
    )

    subparser.add_argument(
        "--max-evals", type=int, default=100000, help="Maximum number of evaluations"
    )
    subparser.add_argument(
        "--num-cpus-per-task",
        type=int,
        default=1,
        help="Number of cores (CPU ressources defined with Ray) per task",
    )
    subparser.add_argument(
        "--num-gpus-per-task",
        type=int,
        default=1,
        help="Number of GPUs (GPU ressources defined with Ray) per task",
    )

    subparser.set_defaults(func=function_to_call)


def main(
    mode,
    search,
    workflow,
    problem,
    run,
    time_minutes,
    nodes,
    queue,
    project,
    max_evals,
    num_cpus_per_task,
    num_gpus_per_task,
    activation_script,
    **kwargs,
):
    """Create & submit the DH search via Balsam"""
    activation_script = os.path.abspath(activation_script)

    # Test if "run", "problem" and "workflow" are correct
    validate(problem, run, workflow)

    # Creation of the submission script

    # Detection of the host
    # hostname = os.environ.get("HOSTNAME", None)
    hostname = "thetagpusn1"
    host = None
    if "thetagpu" in hostname:
        host = "thetagpu"
        print("ThetaGPU detected")
    else:
        print(f"There exist no submission policy for the current system: '{hostname}'")
        exit()

    # Load submission template
    job_template_path = os.path.join(MODULE_PATH, "job-templates-ray", f"{host}.submission.tmpl")

    with open(job_template_path, "r") as f:
        template = Template(f.read())

    # Load script to launch ray cluster template
    current_dir = os.getcwd()
    if nodes > 1:  # mutliple nodes
        launch_ray_path = os.path.join(
            MODULE_PATH, "job-templates-ray", f"{host}.MultiNodesRayCluster.tmpl"
        )
    else:  # single node
        launch_ray_path = os.path.join(
            MODULE_PATH, "job-templates-ray", f"{host}.SingleNodeRayCluster.tmpl"
        )

    with open(launch_ray_path, "r") as f:
        template_launch_ray = Template(f.read())

    # Render script to launch ray cluster
    script_launch_ray_cluster = template_launch_ray.render(
        activation_script=activation_script
    )

    # Render submission template
    submission_path = os.path.join(current_dir, f"sub_{workflow}.sh")
    with open(submission_path, "w") as fp:
        fp.write(
            template.render(
                mode=mode,
                search=search,
                workflow=workflow,
                problem=problem,
                run=run,
                time_minutes=time_minutes,
                nodes=nodes,
                queue=queue,
                project=project,
                max_evals=max_evals,
                num_cpus_per_task=num_cpus_per_task,
                num_gpus_per_task=num_gpus_per_task,
                script_launch_ray_cluster=script_launch_ray_cluster,
            )
        )
        print("Created", fp.name)

    # Job submission
    print("Performing job submission...")
    cmd = f"qsub {submission_path}"
    os.system(f"qsub {submission_path}")

    banner(f"Success. The search will run at: {'TODO'}")


def validate(problem, run, workflow):
    """Validate problem, run, and workflow"""
    current_dir = os.getcwd()

    print("Validating Workflow...", end="", flush=True)
    assert not (
        workflow in os.listdir(current_dir)
    ), f"{workflow} already exist in current directory"
    print("OK", flush=True)

    print("Validating Problem...", end="", flush=True)
    prob = generic_loader(problem, "Problem")
    assert isinstance(prob, (Problem, BaseProblem)), f"{prob} is not a Problem instance"
    print("OK", flush=True)

    print("Validating run...", end="", flush=True)
    run = generic_loader(run, "run")
    assert callable(run), f"{run} must be a a callable"
    print("OK", flush=True)


def render_files(mode, prob_name):
    package = os.path.basename(os.getcwd())
    print("package: ", package)
    templates_pattern = os.path.join(
        os.path.dirname(__file__), "templates", mode, "*.tmpl"
    )
    for template_name in glob.glob(templates_pattern):
        template = Template(open(template_name).read())
        py_name = os.path.basename(template_name.rstrip(".tmpl"))
        with open(os.path.join(prob_name, py_name), "w") as fp:
            fp.write(
                template.render(
                    pckg=package,
                    pb_folder=prob_name,
                )
            )
            print("Created", fp.name)