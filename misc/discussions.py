import os
import time
import requests
import frontmatter

# --- CONFIG ---
# SECURITY: Set this in your terminal: export GITHUB_TOKEN="your_token"
GITHUB_TOKEN = (
    "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"  # OR: os.environ.get("GITHUB_TOKEN")
)

REPO_OWNER = "bittu5134"
REPO_NAME = "lotm-reader"
CATEGORY_SLUG = "COI"
DIRECTORY_PATH = "chapters/coi/webnovel"

# Config for 500 req/hr limit (Safe Mode)
BATCH_SIZE = 50  # How many to create before a long break
BATCH_SLEEP = 300  # 5 minutes sleep between batches
REQUEST_DELAY = 4  # 2 seconds between individual requests

API_URL = "https://api.github.com/graphql"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json",
}


def log_rate_limit(response):
    """Logs the strict rate limit headers from GitHub."""
    limit = response.headers.get("x-ratelimit-limit", "?")
    rem = response.headers.get("x-ratelimit-remaining", "?")
    reset = response.headers.get("x-ratelimit-reset", "?")
    print(f"   [API Limit: {rem}/{limit} remaining. Reset: {reset}]")


def run_query(query, variables=None):
    """Simple GraphQL wrapper with error checking."""
    response = requests.post(
        API_URL,
        json={"query": query, "variables": variables},
        headers=HEADERS,
        timeout=15,
    )

    if response.status_code != 200:
        raise Exception(f"API Error {response.status_code}: {response.text}")

    log_rate_limit(response)

    data = response.json()
    if "errors" in data:
        # Check for abuse detection specifically
        if "too quickly" in str(data["errors"]):
            print("!!! ABUSE DETECTION TRIGGERED. Sleeping 2 mins...")
            time.sleep(120)
            return run_query(query, variables)  # Retry once
        raise Exception(f"GraphQL Error: {data['errors']}")

    return data


def get_repo_info():
    """Fetches Repo ID, Category ID, and ALL existing discussions map."""
    print("Fetching repository data...")
    discussions = {}
    cursor = None
    repo_id, category_id = None, None

    while True:
        query = """
        query($owner: String!, $name: String!, $cursor: String) {
          repository(owner: $owner, name: $name) {
            id
            discussionCategories(first: 10) { nodes { id name } }
            discussions(first: 100, after: $cursor) {
              pageInfo { hasNextPage endCursor }
              nodes { number title category { name } }
            }
          }
        }
        """
        data = run_query(
            query, {"owner": REPO_OWNER, "name": REPO_NAME, "cursor": cursor}
        )["data"]["repository"]

        # Capture IDs on first run
        if not repo_id:
            repo_id = data["id"]
            found_cat = next(
                (
                    c
                    for c in data["discussionCategories"]["nodes"]
                    if c["name"] == CATEGORY_SLUG
                ),
                None,
            )
            if not found_cat:
                raise ValueError(f"Category '{CATEGORY_SLUG}' not found!")
            category_id = found_cat["id"]

        # Collect existing discussions
        for node in data["discussions"]["nodes"]:
            if node["category"]["name"] == CATEGORY_SLUG:
                discussions[node["title"]] = node["number"]

        if not data["discussions"]["pageInfo"]["hasNextPage"]:
            break
        cursor = data["discussions"]["pageInfo"]["endCursor"]

    print(f"Initialized. Found {len(discussions)} existing discussions.\n")
    return repo_id, category_id, discussions


def create_discussion(repo_id, category_id, title, body):
    mutation = """
    mutation($repoId: ID!, $catId: ID!, $title: String!, $body: String!) {
      createDiscussion(input: {repositoryId: $repoId, categoryId: $catId, title: $title, body: $body}) {
        discussion { number }
      }
    }
    """
    data = run_query(
        mutation,
        {"repoId": repo_id, "catId": category_id, "title": title, "body": body},
    )
    return data["data"]["createDiscussion"]["discussion"]["number"]


def main():
    repo_id, category_id, existing_map = get_repo_info()

    # 1. Gather and Sort Files
    files = [
        f for f in os.listdir(DIRECTORY_PATH) if f.endswith(".md") and f != "0000.md"
    ]
    # Sort numerically by chapter number (assuming slug matches filename)
    files.sort(
        key=lambda x: int(
            frontmatter.load(os.path.join(DIRECTORY_PATH, x)).metadata.get("slug", 0)
        )
    )

    created_in_batch = 0

    for filename in files:
        filepath = os.path.join(DIRECTORY_PATH, filename)
        post = frontmatter.load(filepath)

        # SKIP: Already linked locally
        if "discussion" in post.metadata:
            continue

        slug = post.metadata.get("slug")
        title = post.metadata.get("title")
        if not slug or not title:
            continue

        expected_title = f"[COI] CH. {slug} - {title}"

        # SKIP: Already exists on GitHub (just link it)
        if expected_title in existing_map:
            print(f"Linking Existing: {filename} -> #{existing_map[expected_title]}")
            post.metadata["discussion"] = existing_map[expected_title]
            with open(filepath, "wb") as f:
                frontmatter.dump(post, f)
            continue

        # --- RATE LIMIT SAFETY CHECK ---
        if created_in_batch >= BATCH_SIZE:
            print(
                f"\n--- Batch limit ({BATCH_SIZE}) reached. Sleeping {BATCH_SLEEP}s to reset quotas... ---"
            )
            time.sleep(BATCH_SLEEP)
            created_in_batch = 0
            print("--- Resuming ---\n")

        # CREATE
        print(f"Creating: {expected_title} ...")
        body = f"http://beyonder.pages.dev/read/coi/webnovel/{slug}/"

        try:
            disc_num = create_discussion(repo_id, category_id, expected_title, body)

            # Update File
            post.metadata["discussion"] = disc_num
            with open(filepath, "wb") as f:
                frontmatter.dump(post, f)

            print(f"Success! Linked #{disc_num}")
            created_in_batch += 1

            # Short sleep between requests (Secondary limit: max 80/min)
            time.sleep(REQUEST_DELAY)

        except Exception as e:
            print(f"FAILED on {filename}: {e}")
            break  # Stop immediately on error to allow manual fix


if __name__ == "__main__":
    main()
