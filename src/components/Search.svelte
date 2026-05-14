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

const closeFloatingPanel = (): void => {
	const panel = document.getElementById("search-panel");
	panel?.classList.add("float-panel-closed");
};

const scrollResultsBoardIntoView = (): void => {
	window.requestAnimationFrame(() => {
		const board = document.getElementById("search-results-board");
		board?.scrollIntoView({
			behavior: "smooth",
			block: "start",
		});
	});
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

const getCurrentKeyword = (isDesktop: boolean): string =>
	isDesktop ? keywordDesktop : keywordMobile;

const setKeywordValue = (keyword: string, isDesktop: boolean): void => {
	if (isDesktop) {
		keywordDesktop = keyword;
		return;
	}

	keywordMobile = keyword;
};

const setKeywordForBothInputs = (keyword: string): void => {
	keywordDesktop = keyword;
	keywordMobile = keyword;
};

const clearSearchInputs = (): void => {
	setKeywordForBothInputs("");
};

const search = async (keyword: string, isDesktop: boolean): Promise<void> => {
	if (!keyword) {
		closeFloatingPanel();
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
	if (isDesktop) {
		openSearchDisplay();
		closeFloatingPanel();
	}
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

		if (searchToken !== activeSearchToken) {
			return;
		}

		result = searchResults;
		syncBoardState(keyword, { results: searchResults, isSearching: false });
		if (isDesktop) {
			openSearchDisplay();
			closeFloatingPanel();
		}
	} catch (error) {
		if (searchToken !== activeSearchToken) {
			return;
		}

		console.error("Search error:", error);
		result = [];
		syncBoardState(keyword, { results: [], isSearching: false });
		if (isDesktop) {
			openSearchDisplay();
			closeFloatingPanel();
		}
	} finally {
		if (searchToken === activeSearchToken) {
			isSearching = false;
			syncBoardState(keyword, { isSearching: false });
		}
	}
};

const handleKeywordInput = (keyword: string, isDesktop: boolean): void => {
	setKeywordValue(keyword, isDesktop);
	if (!initialized) {
		return;
	}

	void search(keyword, isDesktop);
};

const searchFromUrl = (): void => {
	if (typeof window === "undefined" || !initialized) {
		return;
	}

	const keyword = new URL(window.location.href).searchParams.get("search")?.trim() || "";
	if (!keyword) {
		setKeywordForBothInputs("");
		result = [];
		closeSearchDisplay();
		syncBoardState("", { results: [], isSearching: false });
		return;
	}

	void search(keyword, true);
	clearSearchInputs();
};

const showResultsBoard = (isDesktop: boolean): void => {
	const keyword = getCurrentKeyword(isDesktop).trim();
	if (!keyword) {
		closeSearchDisplay();
		return;
	}

	syncBoardState(keyword, { results, isSearching });
	openSearchDisplay();
	closeFloatingPanel();
	scrollResultsBoardIntoView();
};

const submitSearch = (isDesktop: boolean): void => {
	const keyword = getCurrentKeyword(isDesktop).trim();
	if (!keyword) {
		closeSearchDisplay();
		return;
	}

	showResultsBoard(isDesktop);
	clearSearchInputs();
};

const handleSearchKeydown = (
	event: KeyboardEvent,
	isDesktop: boolean,
): void => {
	if (event.key !== "Enter" || event.isComposing) {
		return;
	}

	event.preventDefault();
	submitSearch(isDesktop);
};

onMount(() => {
	const initializeSearch = () => {
		initialized = true;
		pagefindLoaded =
			typeof window !== "undefined" &&
			!!window.pagefind &&
			typeof window.pagefind.search === "function";
		console.log("Pagefind status on init:", pagefindLoaded);
		searchFromUrl();
	};
	const handlePagefindReady = () => {
		console.log("Pagefind ready event received.");
		initializeSearch();
	};
	const handlePagefindLoadError = () => {
		console.warn(
			"Pagefind load error event received. Search functionality will be limited.",
		);
		initializeSearch();
	};
	let fallbackTimer: ReturnType<typeof window.setTimeout> | undefined;

	if (import.meta.env.DEV) {
		console.log(
			"Pagefind is not available in development mode. Using mock data.",
		);
		initializeSearch();
	} else {
		document.addEventListener("pagefindready", handlePagefindReady);
		document.addEventListener("pagefindloaderror", handlePagefindLoadError);

		// Fallback in case events are not caught or pagefind is already loaded by the time this script runs
		fallbackTimer = window.setTimeout(() => {
			if (!initialized) {
				console.log("Fallback: Initializing search after timeout.");
				initializeSearch();
			}
		}, 2000); // Adjust timeout as needed
	}

	const handlePageLoad = () => {
		searchFromUrl();
	};

	document.addEventListener("astro:page-load", handlePageLoad);

	return () => {
		document.removeEventListener("astro:page-load", handlePageLoad);
		document.removeEventListener("pagefindready", handlePagefindReady);
		document.removeEventListener("pagefindloaderror", handlePagefindLoadError);
		if (fallbackTimer) {
			window.clearTimeout(fallbackTimer);
		}
	};
});
</script>

<!-- search bar for desktop view -->
<div id="search-bar" class="hidden lg:flex relative transition-all items-center h-11 mr-2 rounded-lg
      bg-black/[0.04] hover:bg-black/[0.06] focus-within:bg-black/[0.06]
      dark:bg-white/5 dark:hover:bg-white/10 dark:focus-within:bg-white/10
">
    <Icon icon="material-symbols:search" class="absolute text-[1.25rem] pointer-events-none ml-3 transition my-auto text-black/30 dark:text-white/30"></Icon>
    <input placeholder="{i18n(I18nKey.search)}" bind:value={keywordDesktop} on:focus={() => search(keywordDesktop, true)}
           on:input={(event) => handleKeywordInput((event.currentTarget as HTMLInputElement).value, true)}
           on:keydown={(event) => handleSearchKeydown(event, true)}
           class="transition-all pl-10 text-sm bg-transparent outline-0
          h-full w-40 pr-11 active:w-60 focus:w-60 text-black/50 dark:text-white/50"
    >
    <button
        type="button"
        class="absolute right-1 flex h-9 w-9 items-center justify-center rounded-lg text-black/35 transition hover:bg-black/8 hover:text-black/60 dark:text-white/35 dark:hover:bg-white/10 dark:hover:text-white/70"
        on:click={() => submitSearch(true)}
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
               on:input={(event) => handleKeywordInput((event.currentTarget as HTMLInputElement).value, false)}
               on:keydown={(event) => handleSearchKeydown(event, false)}
               class="pl-10 absolute inset-0 text-sm bg-transparent outline-0
                focus:w-60 text-black/50 dark:text-white/50"
        >
    </div>

    <button
        type="button"
        class="mt-2 flex h-11 w-full items-center justify-center rounded-xl bg-[var(--primary)] text-sm font-semibold text-white transition hover:brightness-105"
        on:click={() => submitSearch(false)}
    >
        在正文区域显示结果
    </button>
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
