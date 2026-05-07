<script lang="ts">
	import { cubicOut, cubicInOut } from "svelte/easing";
	import { fly } from "svelte/transition";

	export let sortedPosts: Post[] = [];
	export let initialTags: string[] = [];
	export let initialCategories: string[] = [];
	export let initialSerieses: string[] = [];
	export let initialUncategorized = false;

	interface Post {
		slug: string;
		collection: "posts" | "notes";
		url: string;
		data: {
			title: string;
			description?: string;
			tags: string[];
			category?: string | null;
			categoryPath?: string[];
			series?: string;
			published: Date | string;
			updated?: Date | string;
		};
	}

	interface FolderNode {
		id: string;
		name: string;
		path: string[];
		parentId: string | null;
		depth: number;
		posts: Post[];
		directPosts: Post[];
		children: FolderNode[];
	}

	const ROOT_FOLDER_ID = "__root__";
	const ROOT_FOLDER_NAME = "全部内容";
	const UNCATEGORIZED_NAME = "未分类";
	const folderLabelCollator = new Intl.Collator("zh-CN", {
		numeric: true,
		sensitivity: "base",
	});

	let tags: string[] = initialTags;
	let categories: string[] = initialCategories;
	let serieses: string[] = initialSerieses;
	let uncategorized = initialUncategorized;

	let archiveRoot: FolderNode = createRootNode();
	let folderLookup = new Map<string, FolderNode>([[ROOT_FOLDER_ID, archiveRoot]]);
	let expandedFolderIds: string[] = [];
	let activeFolderId = ROOT_FOLDER_ID;
	let userChangedTree = false;

	const toDate = (value: Date | string | undefined | null) => {
		if (value instanceof Date) {
			return value;
		}

		const parsed = value ? new Date(value) : new Date(0);
		return Number.isNaN(parsed.getTime()) ? new Date(0) : parsed;
	};

	const sortPosts = (posts: Post[]) =>
		[...posts].sort((a, b) => {
			const timestampDiff =
				toDate(b.data.updated ?? b.data.published).getTime() -
				toDate(a.data.updated ?? a.data.published).getTime();

			if (timestampDiff !== 0) {
				return timestampDiff;
			}

			return folderLabelCollator.compare(a.data.title, b.data.title);
		});

	function createRootNode(): FolderNode {
		return {
		id: ROOT_FOLDER_ID,
		name: ROOT_FOLDER_NAME,
		path: [],
		parentId: null,
		depth: 0,
		posts: [],
		directPosts: [],
		children: [],
		};
	}

	const normalizeFolderSegments = (post: Post) => {
		const pathSegments = (post.data.categoryPath ?? [])
			.map((segment) => segment.trim())
			.filter(Boolean);

		if (pathSegments.length > 0) {
			return pathSegments;
		}

		const category = post.data.category?.trim();
		if (category) {
			return [category];
		}

		return [UNCATEGORIZED_NAME];
	};

	const formatFolderLabel = (label: string) => label;

	const formatFolderTrail = (segments: string[]) =>
		segments.map((segment) => formatFolderLabel(segment)).join(" / ");

	const formatDate = (value: Date | string) => {
		const date = toDate(value);
		const month = `${date.getMonth() + 1}`.padStart(2, "0");
		const day = `${date.getDate()}`.padStart(2, "0");
		return `${month}-${day}`;
	};

	const formatKind = (kind: "posts" | "notes") =>
		kind === "notes" ? "笔记" : "文章";

	const countLabel = (count: number) => `${count} 篇内容`;

	const arraysEqual = (left: string[], right: string[]) =>
		left.length === right.length && left.every((value, index) => value === right[index]);

	const getEntryPathLabel = (post: Post) =>
		formatFolderTrail(normalizeFolderSegments(post));

	const filterPosts = (posts: Post[]) => {
		let filteredPosts = posts;

		if (tags.length > 0) {
			filteredPosts = filteredPosts.filter(
				(post) =>
					Array.isArray(post.data.tags) &&
					post.data.tags.some((tag) => tags.includes(tag)),
			);
		}

		if (categories.length > 0) {
			filteredPosts = filteredPosts.filter(
				(post) => post.data.category && categories.includes(post.data.category),
			);
		}

		if (serieses.length > 0) {
			filteredPosts = filteredPosts.filter(
				(post) => post.data.series && serieses.includes(post.data.series),
			);
		}

		if (uncategorized) {
			filteredPosts = filteredPosts.filter((post) => !post.data.category);
		}

		return sortPosts(filteredPosts);
	};

	const buildArchiveTree = (posts: Post[]) => {
		const root = createRootNode();
		const lookup = new Map<string, FolderNode>([[ROOT_FOLDER_ID, root]]);

		for (const post of sortPosts(posts)) {
			root.posts.push(post);

			let currentNode = root;
			const segments = normalizeFolderSegments(post);

			for (const [index, segment] of segments.entries()) {
				const path = [...currentNode.path, segment];
				const folderId = path.join("::");

				let childNode = lookup.get(folderId);
				if (!childNode) {
					childNode = {
						id: folderId,
						name: segment,
						path,
						parentId: currentNode.id,
						depth: index + 1,
						posts: [],
						directPosts: [],
						children: [],
					};
					lookup.set(folderId, childNode);
					currentNode.children = [...currentNode.children, childNode];
				}

				childNode.posts.push(post);
				currentNode = childNode;
			}

			currentNode.directPosts.push(post);
		}

		const finalizeTree = (node: FolderNode) => {
			node.posts = sortPosts(node.posts);
			node.directPosts = sortPosts(node.directPosts);
			node.children = [...node.children].sort((a, b) => {
				const countDiff = b.posts.length - a.posts.length;
				if (countDiff !== 0) {
					return countDiff;
				}

				return folderLabelCollator.compare(a.name, b.name);
			});
			node.children.forEach(finalizeTree);
		};

		finalizeTree(root);

		return { root, lookup };
	};

	const getDefaultExpandedFolderIds = (root: FolderNode) => {
		const ids = [ROOT_FOLDER_ID];

		for (const child of root.children) {
			if (child.children.length > 0) {
				ids.push(child.id);
			}
		}

		return ids;
	};

	const flattenVisibleFolders = (root: FolderNode, expandedIds: string[]) => {
		const expandedSet = new Set(expandedIds);
		const visibleNodes: FolderNode[] = [];

		const walk = (node: FolderNode) => {
			visibleNodes.push(node);

			if (expandedSet.has(node.id)) {
				node.children.forEach(walk);
			}
		};

		walk(root);
		return visibleNodes;
	};

	const getFolderAncestors = (
		folderId: string,
		lookup: Map<string, FolderNode>,
	) => {
		const ancestors: FolderNode[] = [];
		let currentNode = lookup.get(folderId);

		while (currentNode) {
			ancestors.unshift(currentNode);
			currentNode = currentNode.parentId
				? lookup.get(currentNode.parentId)
				: undefined;
		}

		return ancestors;
	};

	const isDescendantOf = (
		folderId: string,
		possibleAncestorId: string,
		lookup: Map<string, FolderNode>,
	) => {
		let currentNode = lookup.get(folderId);

		while (currentNode) {
			if (currentNode.id === possibleAncestorId) {
				return true;
			}

			currentNode = currentNode.parentId
				? lookup.get(currentNode.parentId)
				: undefined;
		}

		return false;
	};

	const getFolderDisplayPosts = (folder: FolderNode) =>
		folder.directPosts.length > 0 ? folder.directPosts : folder.posts;

	const getFolderSummary = (folder: FolderNode, totalCount: number) => {
		if (folder.id === ROOT_FOLDER_ID) {
			return `当前共归档 ${totalCount} 篇内容，按文件夹路径组织浏览。`;
		}

		if (folder.children.length > 0 && folder.directPosts.length === 0) {
			return `包含 ${folder.children.length} 个子文件夹，合计 ${countLabel(folder.posts.length)}。`;
		}

		return `当前目录共 ${countLabel(getFolderDisplayPosts(folder).length)}。`;
	};

	const getFilterSummary = () => {
		const activeFilters: string[] = [];

		if (categories.length > 0) {
			activeFilters.push(`分类：${categories.join("、")}`);
		}

		if (serieses.length > 0) {
			activeFilters.push(`系列：${serieses.join("、")}`);
		}

		if (tags.length > 0) {
			activeFilters.push(`标签：${tags.join("、")}`);
		}

		if (uncategorized) {
			activeFilters.push("仅未分类内容");
		}

		return activeFilters.join(" / ");
	};

	function ensureFolderTrailExpanded(folderId: string) {
		const expandedSet = new Set(expandedFolderIds);
		const ancestors = getFolderAncestors(folderId, folderLookup);

		for (const node of ancestors) {
			if (node.children.length > 0) {
				expandedSet.add(node.id);
			}
		}

		return [...expandedSet];
	}

	function selectFolder(folderId: string) {
		if (!folderLookup.has(folderId)) {
			return;
		}

		activeFolderId = folderId;
		expandedFolderIds = ensureFolderTrailExpanded(folderId);
		userChangedTree = true;
	}

	function toggleFolder(folderId: string) {
		const folder = folderLookup.get(folderId);
		if (!folder || folder.children.length === 0) {
			return;
		}

		const expandedSet = new Set(expandedFolderIds);
		const shouldCollapse = expandedSet.has(folderId);

		if (shouldCollapse) {
			expandedSet.delete(folderId);

			if (
				activeFolderId !== folderId &&
				isDescendantOf(activeFolderId, folderId, folderLookup)
			) {
				activeFolderId = folderId;
			}
		} else {
			expandedSet.add(folderId);
		}

		expandedFolderIds = [...expandedSet];
		userChangedTree = true;
	}

	$: filteredPosts = filterPosts(sortedPosts);
	$: ({ root: archiveRoot, lookup: folderLookup } = buildArchiveTree(filteredPosts));
	$: {
		const validFolderIds = new Set(folderLookup.keys());
		const hasInvalidExpandedFolder = expandedFolderIds.some(
			(folderId) => !validFolderIds.has(folderId),
		);

		if (!validFolderIds.has(activeFolderId)) {
			activeFolderId = ROOT_FOLDER_ID;
		}

		if (!userChangedTree || expandedFolderIds.length === 0 || hasInvalidExpandedFolder) {
			const nextExpandedFolderIds = getDefaultExpandedFolderIds(archiveRoot);
			if (!arraysEqual(expandedFolderIds, nextExpandedFolderIds)) {
				expandedFolderIds = nextExpandedFolderIds;
			}
		}
	}
	$: visibleFolders = flattenVisibleFolders(archiveRoot, expandedFolderIds);
	$: activeFolder = folderLookup.get(activeFolderId) ?? archiveRoot;
	$: activeFolderAncestors = getFolderAncestors(activeFolder.id, folderLookup);
	$: activeChildFolders = activeFolder.children;
	$: selectedTreeChildFolderIds = new Set(activeChildFolders.map((child) => child.id));
	$: activeFolderPosts = getFolderDisplayPosts(activeFolder);
	$: activeFolderSummary = getFolderSummary(activeFolder, filteredPosts.length);
	$: activeFilterSummary = getFilterSummary();
</script>

<div class="archive-shell">
	<aside class="card-base archive-sidebar">
		<div class="archive-section-head">
			<div>
				<p class="archive-eyebrow">文件夹</p>
				<h2 class="archive-title">正文归档</h2>
			</div>
			<p class="archive-copy">{countLabel(filteredPosts.length)}</p>
		</div>

		<p class="archive-copy">
			{#if activeFilterSummary}
				{activeFilterSummary}
			{:else}
				按 categoryPath 组织目录，优先从大类一路展开到具体题目。
			{/if}
		</p>

		<div class="archive-tree">
			{#each visibleFolders as folder}
				<div class="archive-tree-row" data-active={activeFolderId === folder.id}>
					{#if folder.children.length > 0}
						<button
							type="button"
							class="archive-tree-toggle"
							aria-label={`切换 ${formatFolderLabel(folder.name)} 目录展开状态`}
							aria-expanded={expandedFolderIds.includes(folder.id)}
							on:click={() => toggleFolder(folder.id)}
						>
							<span
								class:list={[
									"archive-tree-chevron",
									{ "archive-tree-chevron--expanded": expandedFolderIds.includes(folder.id) },
								]}
							>
								›
							</span>
						</button>
					{:else}
						<span class="archive-tree-toggle archive-tree-toggle--placeholder"></span>
					{/if}

					<button
						type="button"
						class="archive-tree-button"
						style={`--archive-folder-depth: ${Math.max(folder.depth - 1, 0)};`}
						on:click={() => selectFolder(folder.id)}
					>
						<span class="archive-tree-label">
							<span
								class:list={[
									"archive-tree-icon",
									{
										"archive-tree-icon--filled":
											activeFolderId === folder.id || selectedTreeChildFolderIds.has(folder.id),
									},
								]}
								aria-hidden="true"
							></span>
							<span>{folder.id === ROOT_FOLDER_ID ? ROOT_FOLDER_NAME : formatFolderLabel(folder.name)}</span>
						</span>
						<span class="archive-tree-count">{folder.posts.length}</span>
					</button>
				</div>
			{/each}
		</div>
	</aside>

	<section class="card-base archive-content">
		<div class="archive-section-head">
			<div>
				<p class="archive-eyebrow">当前目录</p>
				<h2 class="archive-title">
					{activeFolder.id === ROOT_FOLDER_ID
						? ROOT_FOLDER_NAME
						: formatFolderLabel(activeFolder.name)}
				</h2>
			</div>
			<p class="archive-copy">{activeFolderSummary}</p>
		</div>

		<nav class="archive-breadcrumbs" aria-label="归档路径">
			{#each activeFolderAncestors as ancestor, index}
				<button
					type="button"
					class="archive-breadcrumb"
					data-active={ancestor.id === activeFolder.id}
					on:click={() => selectFolder(ancestor.id)}
				>
					{ancestor.id === ROOT_FOLDER_ID
						? ROOT_FOLDER_NAME
						: formatFolderLabel(ancestor.name)}
				</button>
				{#if index < activeFolderAncestors.length - 1}
					<span class="archive-breadcrumb-separator">/</span>
				{/if}
			{/each}
		</nav>

		{#key `${activeFolder.id}-${activeFolderPosts.length}-${activeChildFolders.length}`}
			<div
				class="archive-content-stage"
				in:fly={{ y: 14, duration: 320, opacity: 0, easing: cubicOut }}
				out:fly={{ y: -8, duration: 180, opacity: 0, easing: cubicInOut }}
			>
				{#if activeChildFolders.length > 0}
					<section class="archive-block archive-block--grouped">
						<div class="archive-block-head">
							<h3 class="archive-block-title">子文件夹</h3>
							<p class="archive-copy">{activeChildFolders.length} 个</p>
						</div>

						<div class="archive-child-grid">
							{#each activeChildFolders as childFolder}
								<button
									type="button"
									class="archive-child-card"
									on:click={() => selectFolder(childFolder.id)}
								>
									<span class="archive-child-card-label">
										{formatFolderLabel(childFolder.name)}
									</span>
									<span class="archive-child-card-meta">
										{countLabel(childFolder.posts.length)}
									</span>
								</button>
							{/each}
						</div>
					</section>
				{/if}

				<section class="archive-block">
					<div class="archive-block-head">
						<h3 class="archive-block-title">
							{#if activeFolder.id === ROOT_FOLDER_ID}
								全部内容
							{:else if activeFolder.directPosts.length > 0}
								本文件夹正文
							{:else}
								该目录下的正文
							{/if}
						</h3>
						<p class="archive-copy">{countLabel(activeFolderPosts.length)}</p>
					</div>

					{#if activeFolderPosts.length > 0}
						<div class="archive-entry-list">
							{#each activeFolderPosts as post}
								<a href={post.url} class="archive-entry-card" aria-label={post.data.title}>
									<div class="archive-entry-topline">
										<span>{formatDate(post.data.updated ?? post.data.published)}</span>
										<span>{formatKind(post.collection)}</span>
									</div>
									<p class="archive-entry-title">{post.data.title}</p>
									<p class="archive-entry-path">
										{getEntryPathLabel(post)}
										{#if post.data.series}
											<span> · {post.data.series}</span>
										{/if}
									</p>
								</a>
							{/each}
						</div>
					{:else}
						<div class="archive-empty">这里还没有可展示的正文内容。</div>
					{/if}
				</section>
			</div>
		{/key}
	</section>
</div>

<style>
	.archive-shell {
		display: grid;
		grid-template-columns: minmax(0, 18.5rem) minmax(0, 1fr);
		gap: 1rem;
	}

	.archive-sidebar,
	.archive-content {
		padding: 1.15rem;
	}

	.archive-section-head,
	.archive-block-head,
	.archive-entry-topline,
	.archive-tree-row,
	.archive-tree-label,
	.archive-breadcrumbs {
		display: flex;
		align-items: center;
	}

	.archive-section-head,
	.archive-block-head {
		justify-content: space-between;
		gap: 1rem;
	}

	.archive-block-head {
		margin-bottom: 0.85rem;
	}

	.archive-eyebrow {
		margin: 0;
		font-size: 0.72rem;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		color: rgba(71, 85, 105, 0.76);
	}

	.archive-title,
	.archive-block-title {
		margin: 0.3rem 0 0;
		font-weight: 800;
		color: rgba(15, 23, 42, 0.92);
	}

	.archive-title {
		font-size: 1.08rem;
	}

	.archive-block-title {
		font-size: 0.96rem;
	}

	.archive-copy,
	.archive-entry-path,
	.archive-entry-topline,
	.archive-tree-count,
	.archive-breadcrumb-separator {
		color: rgba(71, 85, 105, 0.76);
	}

	.archive-copy {
		margin: 0;
		font-size: 0.84rem;
		line-height: 1.65;
	}

	.archive-tree {
		margin-top: 1rem;
		display: grid;
		gap: 0.3rem;
	}

	.archive-tree-row {
		gap: 0.35rem;
	}

	.archive-tree-toggle,
	.archive-tree-button,
	.archive-child-card,
	.archive-breadcrumb {
		border: 1px solid transparent;
		background: transparent;
		transition:
			background-color 180ms ease,
			border-color 180ms ease,
			transform 180ms ease,
			color 180ms ease,
			box-shadow 180ms ease;
	}

	.archive-tree-toggle {
		display: grid;
		place-items: center;
		width: 2rem;
		height: 2rem;
		padding: 0;
		border-radius: 0.8rem;
		color: rgba(71, 85, 105, 0.76);
		flex-shrink: 0;
	}

	.archive-tree-toggle:hover,
	.archive-tree-button:hover,
	.archive-child-card:hover,
	.archive-breadcrumb:hover {
		background: var(--surface-hover);
		border-color: var(--frame);
	}

	.archive-tree-toggle--placeholder {
		display: inline-block;
	}

	.archive-tree-chevron {
		display: inline-block;
		font-size: 1rem;
		line-height: 1;
		transform: rotate(0deg);
		transition: transform 180ms ease;
	}

	.archive-tree-chevron--expanded {
		transform: rotate(90deg);
	}

	.archive-tree-button {
		flex: 1;
		justify-content: space-between;
		width: 100%;
		padding: 0.72rem 0.8rem;
		border-radius: 0.95rem;
		text-align: left;
		box-shadow: var(--surface-shadow);
	}

	.archive-tree-row[data-active="true"] .archive-tree-button {
		background: var(--surface-hover);
		border-color: var(--frame-strong);
		transform: translateX(2px);
	}

	.archive-tree-button {
		padding-left: calc(0.8rem + (var(--archive-folder-depth, 0) * 0.9rem));
	}

	.archive-tree-label {
		gap: 0.55rem;
		font-size: 0.9rem;
		font-weight: 700;
		color: rgba(15, 23, 42, 0.92);
		overflow: hidden;
	}

	.archive-tree-label span:last-child {
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.archive-tree-icon {
		width: 0.78rem;
		height: 0.78rem;
		border-radius: 0.22rem;
		border: 1px solid var(--frame-strong);
		background: transparent;
		flex-shrink: 0;
		box-shadow: inset 0 0 0 0 rgba(255, 255, 255, 0.88);
		transition:
			background-color 260ms cubic-bezier(0.22, 1, 0.36, 1),
			box-shadow 260ms cubic-bezier(0.22, 1, 0.36, 1),
			border-color 260ms cubic-bezier(0.22, 1, 0.36, 1);
	}

	.archive-tree-icon--filled {
		background: rgba(255, 255, 255, 0.9);
		box-shadow: inset 0 0 0 0.18rem rgba(255, 255, 255, 0.9);
		border-color: rgba(255, 255, 255, 0.96);
	}

	.archive-tree-count {
		font-size: 0.76rem;
		flex-shrink: 0;
	}

	.archive-breadcrumbs {
		flex-wrap: wrap;
		gap: 0.45rem;
		margin-top: 1rem;
		padding-top: 1rem;
		border-top: 1px dashed var(--frame);
	}

	.archive-breadcrumb {
		padding: 0.35rem 0.7rem;
		border-radius: 999px;
		font-size: 0.8rem;
		color: rgba(71, 85, 105, 0.76);
	}

	.archive-breadcrumb[data-active="true"] {
		color: rgba(15, 23, 42, 0.92);
		border-color: var(--frame-strong);
		background: var(--surface-hover);
	}

	.archive-content-stage {
		margin-top: 1rem;
		display: grid;
		gap: 1.1rem;
		min-height: 22rem;
		will-change: transform, opacity, filter;
	}

	.archive-block {
		display: grid;
		gap: 0.85rem;
	}

	.archive-block--grouped {
		padding: 0.95rem 1rem 1rem;
		border: 1px solid var(--frame);
		border-radius: 1rem;
		box-shadow: var(--surface-shadow);
		background: transparent;
	}

	.archive-child-grid {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 0.75rem;
	}

	.archive-child-card {
		display: grid;
		gap: 0.28rem;
		padding: 0.95rem 1rem;
		border-radius: 1rem;
		text-align: left;
		box-shadow: var(--surface-shadow);
	}

	.archive-child-card:hover {
		transform: translateY(-1px);
	}

	.archive-child-card-label {
		font-size: 0.92rem;
		font-weight: 700;
		color: rgba(15, 23, 42, 0.92);
	}

	.archive-child-card-meta {
		font-size: 0.8rem;
		color: rgba(71, 85, 105, 0.76);
	}

	.archive-entry-list {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 0.8rem;
	}

	.archive-entry-card {
		display: grid;
		gap: 0.45rem;
		padding: 1rem;
		border-radius: 1rem;
		border: 1px solid var(--frame);
		box-shadow: var(--surface-shadow);
		text-decoration: none;
		background: transparent;
		transition:
			background-color 180ms ease,
			border-color 180ms ease,
			transform 180ms ease,
			box-shadow 180ms ease;
	}

	.archive-entry-card:hover {
		background: var(--surface-hover);
		border-color: var(--frame-strong);
		transform: translateY(-1px);
	}

	.archive-entry-topline {
		justify-content: space-between;
		gap: 0.85rem;
		font-size: 0.76rem;
	}

	.archive-entry-title {
		margin: 0;
		font-size: 0.98rem;
		font-weight: 800;
		line-height: 1.5;
		color: rgba(15, 23, 42, 0.92);
	}

	.archive-entry-path {
		margin: 0;
		font-size: 0.8rem;
		line-height: 1.6;
	}

	.archive-empty {
		padding: 1.1rem 1rem;
		border-radius: 1rem;
		border: 1px dashed var(--frame);
		color: rgba(71, 85, 105, 0.76);
	}

	:global(.dark) .archive-eyebrow,
	:global(.dark) .archive-copy,
	:global(.dark) .archive-entry-path,
	:global(.dark) .archive-entry-topline,
	:global(.dark) .archive-tree-count,
	:global(.dark) .archive-breadcrumb-separator,
	:global(.dark) .archive-tree-toggle,
	:global(.dark) .archive-breadcrumb,
	:global(.dark) .archive-child-card-meta,
	:global(.dark) .archive-empty {
		color: rgba(203, 213, 225, 0.72);
	}

	:global(.dark) .archive-title,
	:global(.dark) .archive-block-title,
	:global(.dark) .archive-tree-label,
	:global(.dark) .archive-breadcrumb[data-active="true"],
	:global(.dark) .archive-child-card-label,
	:global(.dark) .archive-entry-title {
		color: rgba(248, 250, 252, 0.92);
	}

	:global(.dark) .archive-tree-icon--filled {
		background: rgba(248, 250, 252, 0.92);
		box-shadow: inset 0 0 0 0.18rem rgba(248, 250, 252, 0.92);
		border-color: rgba(248, 250, 252, 0.98);
	}

	@media (max-width: 1100px) {
		.archive-shell {
			grid-template-columns: 1fr;
		}
	}

	@media (max-width: 820px) {
		.archive-child-grid,
		.archive-entry-list {
			grid-template-columns: 1fr;
		}
	}

	@media (max-width: 640px) {
		.archive-sidebar,
		.archive-content {
			padding: 0.95rem;
		}

		.archive-section-head,
		.archive-block-head {
			flex-direction: column;
			align-items: flex-start;
		}

		.archive-tree-button {
			padding-right: 0.72rem;
		}
	}
</style>
