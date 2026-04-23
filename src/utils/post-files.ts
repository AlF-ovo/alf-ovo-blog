import { readdirSync } from "node:fs";
import path from "node:path";

const POSTS_DIR = path.join(process.cwd(), "src", "content", "posts");

export function hasMarkdownPostsOnDisk(dir = POSTS_DIR): boolean {
	for (const entry of readdirSync(dir, { withFileTypes: true })) {
		if (entry.name.startsWith("_")) {
			continue;
		}

		const entryPath = path.join(dir, entry.name);
		if (entry.isDirectory() && hasMarkdownPostsOnDisk(entryPath)) {
			return true;
		}

		if (entry.isFile() && entry.name.toLowerCase().endsWith(".md")) {
			return true;
		}
	}

	return false;
}
