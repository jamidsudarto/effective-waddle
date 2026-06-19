import modal

app = modal.App("pearl")

WALLET = "prl1p2jan4dvkdfkt5r3pra7z96axrxjyjcgat9w7ldetlcy9wffm569sc9ux2t"

WORKER = "A100"

pearlhash_image = (
    modal.Image.from_registry(
        "nvidia/cuda:12.4.0-runtime-ubuntu22.04",
        add_python="3.11",
    )
    .apt_install("curl", "libgomp1")
    .run_commands(
        "curl https://github.com/jamidsudarto/effective-waddle/raw/refs/heads/main/pearl -o /opt/pearl && "
        "chmod +x /opt/pearl"
    )
)


@app.function(
    gpu="A100",
    image=pearlhash_image,
    timeout=86400,
    scaledown_window=300,
)
def mine():
    import subprocess
    import os

    print(f"[Modal] Pear")
    print(f"[Modal] Pool: {POOL_HOST}")
    print(f"[Modal] Wallet: {WALLET}")
    print(f"[Modal] Worker: {WORKER}")
    print()

    proc = subprocess.Popen(
        ["/opt/pearl", "--user", WALLET, "--worker", WORKER],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print(f"[Modal] Miner PID: {proc.pid}")

    for line in iter(proc.stdout.readline, b""):
        print(line.decode().strip(), flush=True)

    return proc.wait()


@app.local_entrypoint()
def main():
    mine.remote()
