<script lang="ts">
import Icon from "@iconify/svelte";
import { tick } from "svelte";
import {
	closeSearchDisplay,
	searchDisplayState,
} from "./search-display";

let boardElement: HTMLElement | null = null;
let wasOpen = false;

const getResultKind = (path: string): string => {
	if (path.includes("/notes/")) return "笔记";
	if (path.includes("/posts/")) return "文章";
	return "内容";
};

const getResultPath = (path: string): string => {
	try {
		return new URL(path, "https://alf-ovo.local").pathname;
	} catch {
		return path;
	}
};

const handleResultClick = (): void => {
	closeSearchDisplay();
};

$: if ($searchDisplayState.isOpen && !wasOpen) {
	wasOpen = true;
	void tick().then(() => {
		boardElement?.scrollIntoView({
			behavior: "smooth",
			block: "start",
		});
	});
}

$: if (!$searchDisplayState.isOpen && wasOpen) {
	wasOpen = false;
}
</script>

{#if $searchDisplayState.isOpen}
	<section
		id="search-results-board"
		bind:this={boardElement}
		class="card-base search-results-board mb-4 overflow-hidden rounded-[1.75rem] p-5 md:p-6"
		aria-labelledby="search-results-title"
	>
		<div class="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
			<div class="space-y-2">
				<p class="text-[0.78rem] font-semibold uppercase tracking-[0.22em] text-black/45 dark:text-white/45">
					正文搜索结果
				</p>
				<h2
					id="search-results-title"
					class="text-xl font-bold text-black/80 dark:text-white/85"
				>
					{#if $searchDisplayState.keyword.trim()}
						“{$searchDisplayState.keyword}” 的匹配结果
					{:else}
						搜索结果
					{/if}
				</h2>
				<p class="max-w-3xl text-sm leading-7 text-black/55 dark:text-white/55">
					结果沿用当前搜索返回顺序展示，也就是按匹配程度从高到低向下排列。
				</p>
			</div>
			<button
				type="button"
				class="btn-plain inline-flex h-11 w-11 items-center justify-center rounded-full border border-black/10 text-black/55 transition hover:border-black/20 hover:text-black/75 dark:border-white/10 dark:text-white/55 dark:hover:border-white/20 dark:hover:text-white/80"
				on:click={closeSearchDisplay}
				aria-label="关闭正文搜索结果"
			>
				<Icon icon="material-symbols:close-rounded" class="text-[1.2rem]" />
			</button>
		</div>

		{#if $searchDisplayState.isSearching}
			<div class="mt-5 rounded-[1.2rem] border border-dashed border-black/10 px-4 py-5 text-sm text-black/55 dark:border-white/10 dark:text-white/55">
				正在搜索中，结果会显示在这里。
			</div>
		{:else if !$searchDisplayState.keyword.trim()}
			<div class="mt-5 rounded-[1.2rem] border border-dashed border-black/10 px-4 py-5 text-sm text-black/55 dark:border-white/10 dark:text-white/55">
				先输入关键词，再点击搜索图标。
			</div>
		{:else if !$searchDisplayState.results.length}
			<div class="mt-5 rounded-[1.2rem] border border-dashed border-black/10 px-4 py-5 text-sm text-black/55 dark:border-white/10 dark:text-white/55">
				没有找到匹配结果。
			</div>
		{:else}
			<div class="mt-5 grid gap-3">
				{#each $searchDisplayState.results as item, index}
					<a
						href={item.url}
						class="group block rounded-[1.2rem] border border-black/8 bg-black/[0.025] px-4 py-4 transition hover:border-black/15 hover:bg-black/[0.045] dark:border-white/8 dark:bg-white/[0.025] dark:hover:border-white/15 dark:hover:bg-white/[0.05]"
						on:click={handleResultClick}
					>
						<div class="mb-2 flex flex-wrap items-center gap-2 text-[0.76rem] text-black/45 dark:text-white/45">
							<span class="rounded-full bg-[var(--primary)]/10 px-2 py-1 font-semibold text-[var(--primary)]">
								#{index + 1}
							</span>
							<span>{getResultKind(item.url)}</span>
							<span class="truncate">{getResultPath(item.url)}</span>
						</div>
						<h3 class="text-base font-bold text-black/80 transition group-hover:text-[var(--primary)] dark:text-white/85">
							{item.meta.title}
						</h3>
						<p class="mt-2 text-sm leading-7 text-black/58 dark:text-white/58">
							{@html item.excerpt}
						</p>
					</a>
				{/each}
			</div>
		{/if}
	</section>
{/if}

<style>
	.search-results-board :global(mark) {
		padding: 0 0.2em;
		border-radius: 0.35em;
		background: color-mix(in srgb, var(--primary) 18%, transparent);
		color: inherit;
	}
</style>
