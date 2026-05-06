<script lang="ts">
import I18nKey from "@i18n/i18nKey";
import { i18n } from "@i18n/translation";
import Icon from "@iconify/svelte";
import { url } from "@utils/url-utils.ts";
import { onMount } from "svelte";
import type { SearchResult } from "@/global";
import {
	closeSearchDisplay,
	openSearchDisplay,
	syncSearchDisplay,
} from "./search/search-display";

let keywordDesktop = "";
let keywordMobile = "";
let result: SearchResult[] = [];
let isSearching = false;
let pagefindLoaded = false;
let initialized = false;
let activeSearchToken = 0;

const fakeResult: SearchResult[] = [
	{
		url: url("/"),
		meta: {
			title: "This Is a Fake Search Result",
		},
		excerpt:
			"Because the search cannot work in the <mark>dev</mark> environment.",
	},
	{
		url: url("/"),
		meta: {
			title: "If You Want to Test the Search",
		},
		excerpt: "Try running <mark>npm build && npm preview</mark> instead.",
	},
];

const togglePanel = () => {
	const panel = document.getElementById("search-panel");
	panel?.classList.toggle("float-panel-closed");
};

const syncBoardState = (
	keyword: string,
	partial: Partial<{ results: SearchResult[]; isSearching: boolean }>,
): void => {
	syncSearchDisplay({
		keyword,
		results: partial.results ?? result,
		isSearching: partial.isSearching ?? isSearching,
	});
};

const setPanelVisibility = (show: boolean, isDesktop: boolean): void => {
	const panel = document.getElementById("search-panel");
	if (!panel || !isDesktop) return;

	panel.classList.add("float-panel-closed");
};

const getCurrentKeyword = (isDesktop: boolean): string =>
	isDesktop ? keywordDesktop : keywordMobile;

const search = async (keyword: string, isDesktop: boolean): Promise<void> => {
	if (!keyword) {
		setPanelVisibility(false, isDesktop);
		result = [];
		closeSearchDisplay();
		syncBoardState("", { results: [], isSearching: false });
		return;
	}

	if (!initialized) {
		return;
	}

	isSearching = true;
	syncBoardState(keyword, { isSearching: true });
	const searchToken = ++activeSearchToken;

	try {
		let searchResults: SearchResult[] = [];

		if (import.meta.env.PROD && pagefindLoaded && window.pagefind) {
			const response = await window.pagefind.search(keyword);
			searchResults = await Promise.all(
				response.results.map((item) => item.data()),
			);
		} else if (import.meta.env.DEV) {
			searchResults = fakeResult;
		} else {
			searchResults = [];
			console.error("Pagefind is not available in production environment.");
		}

		const latestKeyword = getCurrentKeyword(isDesktop);
		if (searchToken !== activeSearchToken || latestKeyword !== keyword) {
			return;
		}

		result = searchResults;
		syncBoardState(keyword, { results: searchResults, isSearching: false });
		setPanelVisibility(result.length > 0, isDesktop);
	} catch (error) {
		const latestKeyword = getCurrentKeyword(isDesktop);
		if (searchToken !== activeSearchToken || latestKeyword !== keyword) {
			return;
		}

		console.error("Search error:", error);
		result = [];
		syncBoardState(keyword, { results: [], isSearching: false });
		setPanelVisibility(false, isDesktop);
	} finally {
		if (searchToken === activeSearchToken) {
			isSearching = false;
			syncBoardState(getCurrentKeyword(isDesktop), { isSearching: false });
		}
	}
};

const showResultsBoard = (isDesktop: boolean): void => {
	const keyword = getCurrentKeyword(isDesktop).trim();
	if (!keyword) {
		closeSearchDisplay();
		return;
	}

	syncBoardState(keyword, { results, isSearching });
	openSearchDisplay();
	setPanelVisibility(false, isDesktop);
};

onMount(() => {
	const initializeSearch = () => {
		initialized = true;
		pagefindLoaded =
			typeof window !== "undefined" &&
			!!window.pagefind &&
			typeof window.pagefind.search === "function";
		console.log("Pagefind status on init:", pagefindLoaded);
		if (keywordDesktop) search(keywordDesktop, true);
		if (keywordMobile) search(keywordMobile, false);
	};

	if (import.meta.env.DEV) {
		console.log(
			"Pagefind is not available in development mode. Using mock data.",
		);
		initializeSearch();
	} else {
		document.addEventListener("pagefindready", () => {
			console.log("Pagefind ready event received.");
			initializeSearch();
		});
		document.addEventListener("pagefindloaderror", () => {
			console.warn(
				"Pagefind load error event received. Search functionality will be limited.",
			);
			initializeSearch(); // Initialize with pagefindLoaded as false
		});

		// Fallback in case events are not caught or pagefind is already loaded by the time this script runs
		setTimeout(() => {
			if (!initialized) {
				console.log("Fallback: Initializing search after timeout.");
				initializeSearch();
			}
		}, 2000); // Adjust timeout as needed
	}
});

$: if (initialized && keywordDesktop) {
	(async () => {
		await search(keywordDesktop, true);
	})();
}

$: if (initialized && keywordMobile) {
	(async () => {
		await search(keywordMobile, false);
	})();
}
</script>

<!-- search bar for desktop view -->
<div id="search-bar" class="hidden lg:flex relative transition-all items-center h-11 mr-2 rounded-lg
      bg-black/[0.04] hover:bg-black/[0.06] focus-within:bg-black/[0.06]
      dark:bg-white/5 dark:hover:bg-white/10 dark:focus-within:bg-white/10
">
    <Icon icon="material-symbols:search" class="absolute text-[1.25rem] pointer-events-none ml-3 transition my-auto text-black/30 dark:text-white/30"></Icon>
    <input placeholder="{i18n(I18nKey.search)}" bind:value={keywordDesktop} on:focus={() => search(keywordDesktop, true)}
           class="transition-all pl-10 text-sm bg-transparent outline-0
         h-full w-40 pr-11 active:w-60 focus:w-60 text-black/50 dark:text-white/50"
    >
    <button
        type="button"
        class="absolute right-1 flex h-9 w-9 items-center justify-center rounded-lg text-black/35 transition hover:bg-black/8 hover:text-black/60 dark:text-white/35 dark:hover:bg-white/10 dark:hover:text-white/70"
        on:click={() => showResultsBoard(true)}
        aria-label="Show search results in main content"
    >
        <Icon icon="material-symbols:search-rounded" class="text-[1.1rem]"></Icon>
    </button>
</div>

<!-- toggle btn for phone/tablet view -->
<button
        on:click={() => {
            if (keywordMobile.trim()) {
                showResultsBoard(false);
                return;
            }
            togglePanel();
        }}
        aria-label="Search Panel" id="search-switch"
        class="btn-plain scale-animation lg:!hidden rounded-lg w-11 h-11 active:scale-90">
    <Icon icon="material-symbols:search" class="text-[1.25rem]"></Icon>
</button>

<!-- search panel -->
<div id="search-panel" class="float-panel float-panel-closed search-panel absolute md:w-[30rem]
top-20 left-4 md:left-[unset] right-4 shadow-2xl rounded-2xl p-2">

    <!-- search bar inside panel for phone/tablet -->
    <div id="search-bar-inside" class="flex relative lg:hidden transition-all items-center h-11 rounded-xl
      bg-black/[0.04] hover:bg-black/[0.06] focus-within:bg-black/[0.06]
      dark:bg-white/5 dark:hover:bg-white/10 dark:focus-within:bg-white/10
  ">
        <Icon icon="material-symbols:search" class="absolute text-[1.25rem] pointer-events-none ml-3 transition my-auto text-black/30 dark:text-white/30"></Icon>
        <input placeholder="Search" bind:value={keywordMobile}
               class="pl-10 absolute inset-0 text-sm bg-transparent outline-0
               focus:w-60 text-black/50 dark:text-white/50"
        >
    </div>

    <button
        type="button"
        class="mt-2 flex h-11 w-full items-center justify-center rounded-xl bg-[var(--primary)] text-sm font-semibold text-white transition hover:brightness-105"
        on:click={() => showResultsBoard(false)}
    >
        在正文区域显示结果
    </button>

    <!-- search results -->
    {#each result as item}
        <a href={item.url}
           class="transition first-of-type:mt-2 lg:first-of-type:mt-0 group block
       rounded-xl text-lg px-3 py-2 hover:bg-[var(--btn-plain-bg-hover)] active:bg-[var(--btn-plain-bg-active)]">
            <div class="transition text-90 inline-flex font-bold group-hover:text-[var(--primary)]">
                {item.meta.title}<Icon icon="fa6-solid:chevron-right" class="transition text-[0.75rem] translate-x-1 my-auto text-[var(--primary)]"></Icon>
            </div>
            <div class="transition text-sm text-50">
                {@html item.excerpt}
            </div>
        </a>
    {/each}
</div>

<style>
  input:focus {
    outline: 0;
  }
  .search-panel {
    max-height: calc(100vh - 100px);
    overflow-y: auto;
  }
</style>
