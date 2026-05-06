import { type CollectionEntry, getCollection } from "astro:content";
import I18nKey from "@i18n/i18nKey";
import { i18n } from "@i18n/translation";
import {
	type ContentCollection,
	getCategoryUrl,
	getCollectionUrl,
} from "@utils/url-utils.ts";

type ContentEntry = CollectionEntry<"posts"> | CollectionEntry<"notes">;

type WrappedEntry<TCollection extends ContentCollection = ContentCollection> = {
	collection: TCollection;
	entry: CollectionEntry<TCollection>;
};

let firstContentPublishedAtPromise: Promise<Date | null> | null = null;

const shouldIncludeEntry = ({ data }: ContentEntry) =>
	import.meta.env.PROD ? data.draft !== true : true;

const sortEntriesByDate = <T extends { entry: ContentEntry }>(entries: T[]) =>
	[...entries].sort((a, b) => {
		const dateA = new Date(a.entry.data.updated ?? a.entry.data.published);
		const dateB = new Date(b.entry.data.updated ?? b.entry.data.published);
		return dateA > dateB ? -1 : 1;
	});

async function getSortedCollectionEntries<TCollection extends ContentCollection>(
	collection: TCollection,
): Promise<CollectionEntry<TCollection>[]> {
	const entries = await getCollection(collection, shouldIncludeEntry);
	const wrappedEntries = sortEntriesByDate(
		entries.map((entry) => ({ collection, entry })),
	);
	return wrappedEntries.map((item) => item.entry as CollectionEntry<TCollection>);
}

export async function getSortedPosts() {
	const sorted = await getSortedCollectionEntries("posts");

	for (let index = 1; index < sorted.length; index++) {
		sorted[index].data.nextSlug = sorted[index - 1].slug;
		sorted[index].data.nextTitle = sorted[index - 1].data.title;
	}

	for (let index = 0; index < sorted.length - 1; index++) {
		sorted[index].data.prevSlug = sorted[index + 1].slug;
		sorted[index].data.prevTitle = sorted[index + 1].data.title;
	}

	return sorted;
}

export function getFirstContentPublishedAt(): Promise<Date | null> {
	if (!firstContentPublishedAtPromise) {
		firstContentPublishedAtPromise = (async () => {
			const [posts, notes] = await Promise.all([
				getCollection("posts", shouldIncludeEntry),
				getCollection("notes", shouldIncludeEntry),
			]);
			const allEntries = [...posts, ...notes];
			if (allEntries.length === 0) {
				return null;
			}

			return allEntries.reduce(
				(earliest, entry) =>
					entry.data.published.getTime() < earliest.getTime()
						? entry.data.published
						: earliest,
				allEntries[0].data.published,
			);
		})();
	}

	return firstContentPublishedAtPromise;
}

export async function getSortedNotes() {
	const sorted = await getSortedCollectionEntries("notes");

	for (let index = 1; index < sorted.length; index++) {
		sorted[index].data.nextSlug = sorted[index - 1].slug;
		sorted[index].data.nextTitle = sorted[index - 1].data.title;
	}

	for (let index = 0; index < sorted.length - 1; index++) {
		sorted[index].data.prevSlug = sorted[index + 1].slug;
		sorted[index].data.prevTitle = sorted[index + 1].data.title;
	}

	return sorted;
}

export async function getAllSortedContentEntries(): Promise<WrappedEntry[]> {
	const [posts, notes] = await Promise.all([getSortedPosts(), getSortedNotes()]);

	return sortEntriesByDate([
		...posts.map((entry) => ({ collection: "posts" as const, entry })),
		...notes.map((entry) => ({ collection: "notes" as const, entry })),
	]);
}

export type ContentForList = {
	slug: string;
	collection: ContentCollection;
	url: string;
	data: ContentEntry["data"];
};

function toListItem<TCollection extends ContentCollection>(
	collection: TCollection,
	entry: CollectionEntry<TCollection>,
): ContentForList {
	return {
		slug: entry.slug,
		collection,
		url: getCollectionUrl(collection, entry.slug),
		data: entry.data,
	};
}

export async function getSortedPostsList(): Promise<ContentForList[]> {
	const sortedPosts = await getSortedPosts();
	return sortedPosts.map((entry) => toListItem("posts", entry));
}

export async function getSortedNotesList(): Promise<ContentForList[]> {
	const sortedNotes = await getSortedNotes();
	return sortedNotes.map((entry) => toListItem("notes", entry));
}

export async function getSortedArchiveEntries(): Promise<ContentForList[]> {
	const entries = await getAllSortedContentEntries();
	return entries.map(({ collection, entry }) => toListItem(collection, entry));
}

export type Tag = {
	name: string;
	count: number;
};

export async function getTagList(): Promise<Tag[]> {
	const allEntries = await getAllSortedContentEntries();
	const countMap: Record<string, number> = {};

	for (const { entry } of allEntries) {
		for (const tag of entry.data.tags) {
			if (!countMap[tag]) {
				countMap[tag] = 0;
			}
			countMap[tag]++;
		}
	}

	return Object.keys(countMap)
		.sort((a, b) => a.toLowerCase().localeCompare(b.toLowerCase()))
		.map((name) => ({ name, count: countMap[name] }));
}

export type Category = {
	name: string;
	count: number;
	url: string;
};

export async function getCategoryList(): Promise<Category[]> {
	const allEntries = await getAllSortedContentEntries();
	const countMap: Record<string, number> = {};

	for (const { entry } of allEntries) {
		if (!entry.data.category) {
			const uncategorizedKey = i18n(I18nKey.uncategorized);
			countMap[uncategorizedKey] = (countMap[uncategorizedKey] || 0) + 1;
			continue;
		}

		const categoryName = entry.data.category.trim();
		countMap[categoryName] = (countMap[categoryName] || 0) + 1;
	}

	return Object.keys(countMap)
		.sort((a, b) => a.toLowerCase().localeCompare(b.toLowerCase()))
		.map((name) => ({
			name,
			count: countMap[name],
			url: getCategoryUrl(name),
		}));
}

export type Series = {
	name: string;
	count: number;
};

export async function getSeriesList(): Promise<Series[]> {
	const allEntries = await getAllSortedContentEntries();
	const countMap: Record<string, number> = {};

	for (const { entry } of allEntries) {
		const series = entry.data.series?.trim();
		if (!series) {
			continue;
		}

		countMap[series] = (countMap[series] || 0) + 1;
	}

	return Object.keys(countMap)
		.sort((a, b) => a.toLowerCase().localeCompare(b.toLowerCase()))
		.map((name) => ({ name, count: countMap[name] }));
}
