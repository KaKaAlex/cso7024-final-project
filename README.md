# Northwind Logistics — Delivery Tracking Service (CSO7024 Final Project starter)

This is the starter application for the **CSO7024 DevOps** final project. It is
a small, working delivery-tracking web service for the fictional company **Northwind
Logistics**. The scenario is described below; the full Final Project brief on Canvas
sets out exactly what you must build and how it is marked.

Your task is to wrap a complete DevOps toolchain around this service: version
control, automated tests, a Continuous Integration and Continuous Deployment
(CI/CD) pipeline, configuration management or Infrastructure as Code, and
containerisation with orchestration. **Keep changes to the application itself
modest** — the focus of the project is the workflow around the code, not new
features.

## Scenario

Northwind Logistics is the mid-sized European logistics provider from the module's
case studies. Among its systems is the delivery-tracking service in this
repository, which lets operators and customers check the status of a parcel in
transit. Like the rest of Northwind's platform, it is deployed frequently and is
expected to be reliable, so the team wants it put on a firm DevOps footing:
automated testing, a repeatable build-and-deploy pipeline, a reproducible
environment, and a containerised, orchestrated deployment. Acting as the DevOps
engineer for this service, you will build that toolchain around the provided
application and evaluate it in a technical report.

## What the service does

It exposes a small HTTP API for checking the status of deliveries. The data is
held in memory, so the service runs with no database or other external
dependency.

| Method | Path                | Description                                  |
| ------ | ------------------- | -------------------------------------------- |
| GET    | `/`                 | Service information and the list of endpoints |
| GET    | `/health`           | Health check, always returns HTTP 200         |
| GET    | `/deliveries`       | All deliveries, as JSON                        |
| GET    | `/deliveries/{id}`  | One delivery as JSON, or HTTP 404 if unknown  |

The `/health` endpoint exists so you can wire up a container health check and
Kubernetes readiness and liveness probes.

## Before you start

You need **Python 3.10 or newer** and **Git**. To complete the later steps of the
brief you will also need **Docker** and a single-node Kubernetes tool (**minikube**
or **k3s**), and, depending on the path you choose, **Terraform** or **Ansible**.
You do not need any paid cloud accounts.

## Run it locally

The service uses only the Python standard library, so there is nothing to install
to run it:

```bash
python -m app
# or, equivalently:
python run.py
```

Then, in another terminal:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/deliveries
curl http://localhost:8000/deliveries/NL-1002
```

The port can be changed with the `PORT` environment variable, for example
`PORT=9000 python -m app`.

## Project layout

```
app/
  __main__.py   lets you run the service with `python -m app`
  service.py    the HTTP request handler and server
  data.py       the in-memory delivery records
run.py          convenience entry point (`python run.py`)
requirements.txt
```

## Deploying this service locally: two things to plan for

These points trip people up when building a pipeline around a service that runs
on a single-node local cluster. Neither is solved for you; decide how you will
handle each, and explain your choice in your report.

**A cloud-hosted CI runner cannot reach your local cluster.** GitHub Actions and
GitLab's hosted runners run on the provider's infrastructure, with no network
route to a minikube or k3s cluster on your own machine. A hosted pipeline can
build the image, run the tests and push the image to a container registry, but
applying it to your cluster (for example, with `kubectl apply`) happens on your
machine. You can meet the brief's deployment stage either by having the pipeline
publish the image to a registry that your local deployment then pulls from, or by
running a self-hosted runner if you want the pipeline itself to deploy.

**"Automating the environment" with no cloud account.** Everything here runs
locally, so be deliberate about what your configuration management or
Infrastructure as Code actually does. Ansible fits naturally for installing
dependencies and configuring the environment the service runs in. If you use
Terraform, be clear about which local resources it manages — for example, Docker
or Kubernetes objects through the relevant provider — rather than cloud
infrastructure that is not part of this setup, and keep the boundary between this
step and your Kubernetes deployment explicit so the two do not overlap.

## A note on dependencies and testing

The application has no runtime dependencies. When you build your automated test
suite (step 3 of the brief), add your testing tool — for example `pytest` — to
`requirements.txt` and pin it.
