import type { SearchResult } from "@/global";
import { writable } from "svelte/store";

export interface SearchDisplayState {
	keyword: string;
	results: SearchResult[];
	isSearching: boolean;
	isOpen: boolean;
}

const initialState: SearchDisplayState = {
	keyword: "",
	results: [],
	isSearching: false,
	isOpen: false,
};

export const searchDisplayState = writable<SearchDisplayState>(initialState);

export const syncSearchDisplay = (
	partial: Partial<SearchDisplayState>,
): void => {
	searchDisplayState.update((state) => ({ ...state, ...partial }));
};

export const openSearchDisplay = (): void => {
	syncSearchDisplay({ isOpen: true });
};

export const closeSearchDisplay = (): void => {
	syncSearchDisplay({ isOpen: false });
};

export const resetSearchDisplay = (): void => {
	searchDisplayState.set(initialState);
};
