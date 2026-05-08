import { getCategoryList, getAllSortedContentEntries, getSeriesList } from "./content-utils";
import { getCollectionUrl } from "./url-utils";

type VisitGrowthPoint = {
	label: string;
	bucketKey: string;
	totalVisits: number;
	growthRate: number;
};

type VisitGrowthDataset = {
	label: string;
	points: VisitGrowthPoint[];
};

type DashboardRecentUpdate = {
	title: string;
	time: string;
	url: string;
	description: string;
	kindLabel: "文章" | "笔记";
};

type DashboardEntrySummary = {
	title: string;
	url: string;
	excerpt: string;
	kindLabel: "文章" | "笔记" | "内容";
};

type DashboardMetrics = {
	updatedEntries: number;
	updatedWords: number;
	contentBreakdown: string;
	contentBreakdownNote: string;
	lastUpdatedEntry: DashboardEntrySummary;
	latestPost: DashboardEntrySummary;
	latestNote: DashboardEntrySummary;
};

type DashboardData = {
	chartDatasets: Record<"week" | "month" | "year", VisitGrowthDataset>;
	recentUpdates: DashboardRecentUpdate[];
	dashboardMetrics: DashboardMetrics;
};

type WrappedEntry = Awaited<ReturnType<typeof getAllSortedContentEntries>>[number];

const DASHBOARD_FALLBACK_ENTRY: DashboardEntrySummary = {
	title: "暂无内容",
	url: "/archive/",
	excerpt: "当前还没有可展示的内容。",
	kindLabel: "内容",
};

const formatDateTime = (date: Date) =>
	new Intl.DateTimeFormat("zh-CN", {
		year: "numeric",
		month: "2-digit",
		day: "2-digit",
		hour: "2-digit",
		minute: "2-digit",
		hour12: false,
	}).format(date);

const getKindLabel = (
	collection: WrappedEntry["collection"],
): DashboardRecentUpdate["kindLabel"] =>
	collection === "notes" ? "笔记" : "文章";

const toEntrySummary = (entry?: WrappedEntry): DashboardEntrySummary => {
	if (!entry) {
		return DASHBOARD_FALLBACK_ENTRY;
	}

	return {
		title: entry.entry.data.title,
		url: getCollectionUrl(entry.collection, entry.entry.slug),
		excerpt: entry.entry.data.description || "这条内容暂时还没有摘要。",
		kindLabel: getKindLabel(entry.collection),
	};
};

const getWordCount = (content: string) => {
	const latinWords = content.match(/[A-Za-z0-9_]+/g)?.length ?? 0;
	const cjkChars = content.match(/[\u3400-\u9fff]/g)?.length ?? 0;
	return latinWords + cjkChars;
};

const getEntryDisplayDate = (entry: WrappedEntry) =>
	new Date(entry.entry.data.updated ?? entry.entry.data.published);

const startOfDay = (date: Date) =>
	new Date(date.getFullYear(), date.getMonth(), date.getDate());

const formatDayKey = (date: Date) => {
	const year = date.getFullYear();
	const month = `${date.getMonth() + 1}`.padStart(2, "0");
	const day = `${date.getDate()}`.padStart(2, "0");
	return `${year}-${month}-${day}`;
};

const formatMonthKey = (date: Date) => {
	const year = date.getFullYear();
	const month = `${date.getMonth() + 1}`.padStart(2, "0");
	return `${year}-${month}`;
};

const createDaySeries = (length: number, endDate: Date) => {
	const dates: Date[] = [];
	const normalizedEnd = startOfDay(endDate);

	for (let index = length - 1; index >= 0; index--) {
		const current = new Date(normalizedEnd);
		current.setDate(normalizedEnd.getDate() - index);
		dates.push(current);
	}

	return dates;
};

const createMonthSeries = (length: number, endDate: Date) => {
	const dates: Date[] = [];
	const normalizedEnd = new Date(endDate.getFullYear(), endDate.getMonth(), 1);

	for (let index = length - 1; index >= 0; index--) {
		const current = new Date(normalizedEnd);
		current.setMonth(normalizedEnd.getMonth() - index);
		dates.push(current);
	}

	return dates;
};

const buildVisitDatasetFromDays = (
	label: string,
	dates: Date[],
): VisitGrowthDataset => ({
	label,
	points: dates.map((date) => ({
		label: `${`${date.getMonth() + 1}`.padStart(2, "0")}/${`${date.getDate()}`.padStart(2, "0")}`,
		bucketKey: formatDayKey(date),
		totalVisits: 0,
		growthRate: 0,
	})),
});

const buildVisitDatasetFromMonths = (
	label: string,
	dates: Date[],
): VisitGrowthDataset => ({
	label,
	points: dates.map((date) => ({
		label: `${date.getMonth() + 1}月`,
		bucketKey: formatMonthKey(date),
		totalVisits: 0,
		growthRate: 0,
	})),
});

export async function getDashboardData(): Promise<DashboardData> {
	const allEntries = await getAllSortedContentEntries();
	const categories = await getCategoryList();
	const seriesList = await getSeriesList();

	const posts = allEntries.filter((entry) => entry.collection === "posts");
	const notes = allEntries.filter((entry) => entry.collection === "notes");

	const thirtyDaysAgo = startOfDay(new Date());
	thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 29);

	const updatedEntries = allEntries.filter(
		(entry) => getEntryDisplayDate(entry).getTime() >= thirtyDaysAgo.getTime(),
	);

	const updatedWords = updatedEntries.reduce(
		(sum, entry) => sum + getWordCount(String(entry.entry.body || "")),
		0,
	);

	const recentUpdates = allEntries.slice(0, 8).map((entry) => ({
		title: entry.entry.data.title,
		time: formatDateTime(getEntryDisplayDate(entry)),
		url: getCollectionUrl(entry.collection, entry.entry.slug),
		description: entry.entry.data.description || "这条内容暂时还没有摘要。",
		kindLabel: getKindLabel(entry.collection),
	}));

	const categorySummary = categories
		.slice(0, 3)
		.map((category) => `${category.name} ${category.count} 条`)
		.join("，");

	const now = new Date();

	return {
		chartDatasets: {
			week: buildVisitDatasetFromDays("近 7 天", createDaySeries(7, now)),
			month: buildVisitDatasetFromDays("近 30 天", createDaySeries(30, now)),
			year: buildVisitDatasetFromMonths("近 12 个月", createMonthSeries(12, now)),
		},
		recentUpdates,
		dashboardMetrics: {
			updatedEntries: updatedEntries.length,
			updatedWords,
			contentBreakdown: `${posts.length} 篇文章 / ${notes.length} 条笔记`,
			contentBreakdownNote: `当前共 ${categories.length} 个分类${seriesList.length > 0 ? `，${seriesList.length} 个系列` : ""}${categorySummary ? `，重点分类：${categorySummary}` : ""}`,
			lastUpdatedEntry: toEntrySummary(allEntries[0]),
			latestPost: toEntrySummary(posts[0]),
			latestNote: toEntrySummary(notes[0]),
		},
	};
}
