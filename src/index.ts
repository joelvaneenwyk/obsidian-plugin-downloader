// Used to fetch community-plugins.json, may be changed to something different in future, like "got".
import fetch from "node-fetch";
import { download, extract } from "gitly";
import cliProgress from "cli-progress";
import ora from "ora";

import { spawn, Pool, Worker } from "threads"

/** Pool event type. Specifies the type of each `PoolEvent`. */
export enum PoolEventType {
  initialized = "initialized",
  taskCanceled = "taskCanceled",
  taskCompleted = "taskCompleted",
  taskFailed = "taskFailed",
  taskQueued = "taskQueued",
  taskQueueDrained = "taskQueueDrained",
  taskStart = "taskStart",
  terminated = "terminated"
}

const URLS = {
  COMMUNITY_PLUGINS:
    "https://raw.githubusercontent.com/obsidianmd/obsidian-releases/master/community-plugins.json",
};

interface GitlyError {
  code?: number
}

/** Download repository and fallback to other branch if it doesn't use `master`. */
async function downloadRepo(repo:string): Promise<void> {
  let source: string;

  // Fallback to main branch if master doesn't work. The default in `gitly` is `master` and most Obsidian repositories use it.
  try {
    // Try to download from `master` branch.
    source = await download(repo, { throw: true });
  } catch (error: unknown) {
    // If not found, try to download from main brach. Else it's an other error.
    const gitlyError = error as GitlyError;
    if (gitlyError.code === 404) {
      source = await download(`${repo}#main`, { throw: true });
    } else {
      console.error(error);
      throw error;
    }
  }

  await extract(source, `repositories/${repo}`);
}

/** Downloads GitHub repositories that aren't already downloaded, creating a tree structure. */
async function downloadRepositories(repos: string[]): Promise<void> {
  const downloadBar = new cliProgress.SingleBar({
    format: "[{bar}] {percentage}% | {value}/{total} | 📂 {repo}",
    hideCursor: true,
  }, cliProgress.Presets.shades_classic);

  downloadBar.start(repos.length, 0);

  for await (const repo of repos) {
    await downloadRepo(repo);
    downloadBar.increment({ repo: repo });
  }

  downloadBar.stop();
}

interface Plugin {
  id: string;
  name: string;
  author: string;
  description: string;
  repo: string;
}

type Plugins = Plugin[];

/** Return list of plugin repositories on GitHub. */
async function getPluginsRepos() {
  const spinner = ora("Fetching community-plugins.json").start();

  // Fetch community-plugins.json and turn it into object
  const response = await fetch(URLS.COMMUNITY_PLUGINS);
  const communityPluginsJson: Plugins = await response.json() as Plugins

  // Get "repo" from every plugin.
  const pluginsRepos = communityPluginsJson.map((plugin) => plugin.repo);

  spinner.succeed(`Found ${pluginsRepos.length} plugins!`);

  // [author/plugin_name, author2/plugin_name3...]
  return pluginsRepos;
}

export default async function main() {
  const events: Pool.Event[] = []
  let spawnCalled = 0
  let taskFnCalled = 0

  const spawnWorker = () => {
    spawnCalled++
    return spawn<() => string>(new Worker("./worker"))
  }
  const pool = Pool(spawnWorker, 20)
  pool.events().subscribe(event => events.push(event))

  // Just to make sure all worker threads are initialized before starting to queue
  // This is only necessary for testing to make sure that this is the first event recorded
  await new Promise((resolve, reject) => {
    pool.events()
      .filter(event => event.type === PoolEventType.initialized)
      .subscribe(resolve, reject)
  })

  await pool.queue(async workerTask => {
    taskFnCalled++
    const result = await workerTask()
    console.log(result);
    return result
  })

  await pool.terminate()

  return;

  getPluginsRepos().then((repos) => downloadRepositories(repos));
}

await main();
