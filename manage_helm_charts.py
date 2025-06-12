import argparse
import requests
import subprocess
from tabulate import tabulate

ARTIFACT_HUB_API = "https://artifacthub.io/api/v1"

def search_charts(keyword):
    url = f"{ARTIFACT_HUB_API}/packages/search?kind=0&limit=10&ts_query_web={keyword}"
    response = requests.get(url)
    if response.status_code != 200:
        print("Error al buscar charts en Artifact Hub.")
        return
    results = response.json().get('packages', [])
    table = []
    for pkg in results:
        table.append([pkg["name"], pkg["repository"]["name"], pkg["version"], pkg["description"][:50]])
    print(tabulate(table, headers=["Name", "Repo", "Version", "Description"]))

def get_chart_info(pkg_name):
    repo, chart = pkg_name.split("/")
    url = f"{ARTIFACT_HUB_API}/packages/helm/{repo}/{chart}"
    response = requests.get(url)
    if response.status_code != 200:
        print("Chart no encontrado.")
        return
    pkg = response.json()
    print(f"\nName: {pkg['name']}")
    print(f"Version: {pkg['version']}")
    print(f"Description: {pkg['description']}")
    print(f"Repo URL: {pkg['repository']['url']}")
    print(f"Maintainers: {', '.join([m['name'] for m in pkg.get('maintainers', [])])}\n")

def add_repo(repo_name, repo_url):
    subprocess.run(["helm", "repo", "add", repo_name, repo_url])
    subprocess.run(["helm", "repo", "update"])

def install_chart(pkg_name, release, version=None, namespace="default"):
    repo, chart = pkg_name.split("/")
    # Get chart info to extract the repo URL
    url = f"{ARTIFACT_HUB_API}/packages/helm/{repo}/{chart}"
    response = requests.get(url)
    repo_url = response.json()["repository"]["url"]
    add_repo(repo, repo_url)

    cmd = ["helm", "upgrade", "--install", release, f"{repo}/{chart}", "--namespace", namespace]
    if version:
        cmd += ["--version", version]
    subprocess.run(["kubectl", "create", "namespace", namespace], stderr=subprocess.DEVNULL)
    subprocess.run(cmd)

def list_releases(namespace=None):
    cmd = ["helm", "list", "--all"]
    if namespace:
        cmd += ["--namespace", namespace]
    subprocess.run(cmd)

def uninstall_release(release, namespace="default"):
    subprocess.run(["helm", "uninstall", release, "--namespace", namespace])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Helm Chart Manager")
    subparsers = parser.add_subparsers(dest="command")

    s = subparsers.add_parser("search")
    s.add_argument("keyword")

    i = subparsers.add_parser("info")
    i.add_argument("chart")

    inst = subparsers.add_parser("install")
    inst.add_argument("chart")
    inst.add_argument("--release", required=True)
    inst.add_argument("--version", required=False)
    inst.add_argument("--namespace", default="default")

    l = subparsers.add_parser("list-releases")
    l.add_argument("--namespace", required=False)

    u = subparsers.add_parser("uninstall")
    u.add_argument("release")
    u.add_argument("--namespace", default="default")

    args = parser.parse_args()

    if args.command == "search":
        search_charts(args.keyword)
    elif args.command == "info":
        get_chart_info(args.chart)
    elif args.command == "install":
        install_chart(args.chart, args.release, args.version, args.namespace)
    elif args.command == "list-releases":
        list_releases(args.namespace)
    elif args.command == "uninstall":
        uninstall_release(args.release, args.namespace)
