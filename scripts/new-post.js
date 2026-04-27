import fs from "node:fs";
import path from "node:path";

function getDate() {
	const today = new Date();
	const year = today.getFullYear();
	const month = String(today.getMonth() + 1).padStart(2, "0");
	const day = String(today.getDate()).padStart(2, "0");

	return `${year}-${month}-${day}`;
}

function printUsage() {
	console.error(`Usage:
  pnpm new-post -- <slug>
  pnpm new-post -- <slug> --type note

Default behavior:
  - creates a bundled content directory
  - posts go to src/content/posts/<slug>/index.md
  - notes go to src/content/notes/<slug>/index.md`);
}

const args = process.argv.slice(2);

if (args.length === 0) {
	printUsage();
	process.exit(1);
}

let slug = "";
let contentType = "post";

for (let index = 0; index < args.length; index++) {
	const current = args[index];
	if (current === "--type") {
		contentType = args[index + 1] || "";
		index++;
		continue;
	}

	if (!slug) {
		slug = current;
	}
}

if (!slug) {
	printUsage();
	process.exit(1);
}

if (!["post", "note"].includes(contentType)) {
	console.error(`Unsupported content type: ${contentType}`);
	process.exit(1);
}

const collectionDir = contentType === "note" ? "notes" : "posts";
const targetDir = path.join("src", "content", collectionDir, slug);
const fullPath = path.join(targetDir, "index.md");

if (fs.existsSync(fullPath)) {
	console.error(`Error: File ${fullPath} already exists`);
	process.exit(1);
}

fs.mkdirSync(targetDir, { recursive: true });

const content = `---
title: "${slug}"
published: ${getDate()}
description: ""
image: ""
tags: []
category: ""
categoryPath: []
series: ""
draft: false
lang: "zh_CN"
---

`;

fs.writeFileSync(fullPath, content);

console.log(`Created ${contentType} at ${fullPath}`);
