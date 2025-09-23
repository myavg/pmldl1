from pathlib import Path
import docker
import time

ROOT = Path(__file__).resolve().parents[2]
DOCKERFILE = ROOT / "Dockerfile"
PROJECT = "wine"
NET = f"{PROJECT}_net"
API_IMAGE = f"{PROJECT}_api:latest"
APP_IMAGE = f"{PROJECT}_app:latest"
API_CONT = "wine_api"
APP_CONT = "wine_app"

def ensure_network(client):
    nets = [n.name for n in client.networks.list()]
    if NET not in nets:
        client.networks.create(NET)
    return client.networks.get(NET)

def build_image(client, target, tag):
    print(f"[Stage 3] Building {tag} (target={target}) ...")
    # low-level API to stream output
    for chunk in client.api.build(
        path=str(ROOT),
        dockerfile=str(DOCKERFILE.relative_to(ROOT)),
        target=target,
        tag=tag,
        decode=True
    ):
        if "stream" in chunk:
            line = chunk["stream"].strip()
            if line:
                print(line)

def recreate_container(client, name, image, **run_kwargs):
    # stop & remove if exists
    try:
        c = client.containers.get(name)
        print(f"[Stage 3] Removing existing container {name} ...")
        c.remove(force=True)
    except docker.errors.NotFound:
        pass
    print(f"[Stage 3] Creating container {name} ...")
    return client.containers.run(image, name=name, detach=True, **run_kwargs)

def main():
    client = docker.from_env()
    net = ensure_network(client)

    build_image(client, target="api", tag=API_IMAGE)
    build_image(client, target="app", tag=APP_IMAGE)

    # API
    api = recreate_container(
        client,
        API_CONT,
        API_IMAGE,
        ports={"8000/tcp": 8000},
        network=NET,
        restart_policy={"Name": "unless-stopped"},
    )

    # App
    app = recreate_container(
        client,
        APP_CONT,
        APP_IMAGE,
        ports={"8501/tcp": 8501},
        network=NET,
        environment={"API_URL": "http://wine_api:8000"},
        restart_policy={"Name": "unless-stopped"},
    )

    time.sleep(2)
    print(f"[Stage 3] Containers are up: {API_CONT} (8000), {APP_CONT} (8501)")

if __name__ == "__main__":
    main()
