import { readdirSync } from "node:fs";
import path from "node:path";

const POSTS_DIR = path.join(process.cwd(), "src", "content", "posts");
const NOTES_DIR = path.join(process.cwd(), "src", "content", "notes");

export function hasMarkdownEntriesOnDisk(dir: string): boolean {
	for (const entry of readdirSync(dir, { withFileTypes: true })) {
		if (entry.name.startsWith("_")) {
			continue;
		}

		const entryPath = path.join(dir, entry.name);
		if (entry.isDirectory() && hasMarkdownEntriesOnDisk(entryPath)) {
			return true;
		}

		if (entry.isFile() && entry.name.toLowerCase().endsWith(".md")) {
			return true;
		}
	}

	return false;
}

export function hasMarkdownPostsOnDisk() {
	return hasMarkdownEntriesOnDisk(POSTS_DIR);
}

export function hasMarkdownNotesOnDisk() {
	return hasMarkdownEntriesOnDisk(NOTES_DIR);
}
