# Step 7. Download your Kubernetes corpus
import os
import requests
from markdownify import markdownify as md
from pathlib import Path
pages = {
    "architecture":  "https://kubernetes.io/docs/concepts/architecture/",
    "components":    "https://kubernetes.io/docs/concepts/overview/components/",
    "nodes":         "https://kubernetes.io/docs/concepts/architecture/nodes/",
    "pods":          "https://kubernetes.io/docs/concepts/workloads/pods/",
    "workloads":     "https://kubernetes.io/docs/concepts/workloads/",
    "deployments":   "https://kubernetes.io/docs/concepts/workloads/controllers/deployment/",
    "replicasets":   "https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/",
    "services":      "https://kubernetes.io/docs/concepts/services-networking/service/",
    "networking":    "https://kubernetes.io/docs/concepts/services-networking/",
    "storage":       "https://kubernetes.io/docs/concepts/storage/",
    "configmaps":    "https://kubernetes.io/docs/concepts/configuration/configmap/",
    "secrets":       "https://kubernetes.io/docs/concepts/configuration/secret/",
    "scheduling":    "https://kubernetes.io/docs/concepts/scheduling-eviction/",
    "controllers":   "https://kubernetes.io/docs/concepts/workloads/controllers/",
}
PROJECT_ROOT = Path(__file__).resolve().parent.parent # app/ --> project/
DATA_DIR = PROJECT_ROOT / "data" / "raw"

DATA_DIR.mkdir(exist_ok=True, parents=True)
# os.makedirs("app/data/raw", exist_ok=True)

for name, url in pages.items():
    html = requests.get(url).text
    # Strip nav/footer — keep only <main> content
    start = html.find("<main")
    end = html.find("</main>")
    if start != -1 and end != -1:
        html = html[start:end + len("</main>")]
    # with open(f"{DATA_DIR}/{name}.md", "w", encoding="utf-8") as f:
        # f.write(md(html, strip=["nav", "footer", "header"]))
    (DATA_DIR / f"{name}.md").write_text(md(html, strip=["nav", "footer", "header"]), encoding="utf-8")
    print(f"✓ {name}.md")

print(f"\nDone — {len(pages)} files in data/raw/")