import { execSync } from "node:child_process";
import { getCategoryList, getAllSortedContentEntries, getSeriesList } from "./content-utils";
import { getCollectionUrl } from "./url-utils";

type ActivityPoint = {
	label: string;
	publish: number;
	update: number;
	delete: number;
};

type ActivityDataset = {
	label: string;
	points: ActivityPoint[];
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
	chartDatasets: Record<"week" | "month" | "year", ActivityDataset>;
	recentUpdates: DashboardRecentUpdate[];
	dashboardMetrics: DashboardMetrics;
};

type WrappedEntry = Awaited<ReturnType<typeof getAllSortedContentEntries>>[number];

type GitDayStats = {
	publish: number;
	update: number;
	delete: number;
};

const DASHBOARD_FALLBACK_ENTRY: DashboardEntrySummary = {
	title: "暂无内容",
	url: "/archive/",
	excerpt: "当前还没有可展示的内容。",
	kindLabel: "内容",
};

const isMarkdownContentPath = (filePath: string) =>
	/\.md$/i.test(filePath) &&
	(filePath.includes("src/content/posts/") ||
		filePath.includes("src/content/notes/") ||
		filePath.includes("src\\content\\posts\\") ||
		filePath.includes("src\\content\\notes\\"));

const formatDateTime = (date: Date) =>
	new Intl.DateTimeFormat("zh-CN", {
		year: "numeric",
		month: "2-digit",
		day: "2-digit",
		hour: "2-digit",
		minute: "2-digit",
		hour12: false,
	}).format(date);

const getKindLabel = (collection: WrappedEntry["collection"]) =>
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

const parseGitActivity = () => {
	const dayStats = new Map<string, GitDayStats>();

	try {
		const output = execSync(
			'git log --name-status --find-renames --date=short --format="commit %H %ad" -- src/content/posts src/content/notes',
			{
				encoding: "utf8",
				stdio: ["ignore", "pipe", "ignore"],
			},
		);

		let activeDayKey = "";

		for (const rawLine of output.split(/\r?\n/)) {
			const line = rawLine.trim();

			if (!line) {
				continue;
			}

			if (line.startsWith("commit ")) {
				const parts = line.split(/\s+/);
				activeDayKey = parts[2] || "";
				if (activeDayKey && !dayStats.has(activeDayKey)) {
					dayStats.set(activeDayKey, { publish: 0, update: 0, delete: 0 });
				}
				continue;
			}

			if (!activeDayKey) {
				continue;
			}

			const parts = rawLine.split("\t");
			const status = parts[0]?.trim() || "";
			const stats = dayStats.get(activeDayKey);

			if (!stats) {
				continue;
			}

			if (status.startsWith("A")) {
				const filePath = parts[1] || "";
				if (isMarkdownContentPath(filePath)) {
					stats.publish += 1;
				}
				continue;
			}

			if (status.startsWith("M")) {
				const filePath = parts[1] || "";
				if (isMarkdownContentPath(filePath)) {
					stats.update += 1;
				}
				continue;
			}

			if (status.startsWith("D")) {
				const filePath = parts[1] || "";
				if (isMarkdownContentPath(filePath)) {
					stats.delete += 1;
				}
				continue;
			}

			if (status.startsWith("R") || status.startsWith("C")) {
				const targetPath = parts[2] || parts[1] || "";
				if (isMarkdownContentPath(targetPath)) {
					stats.update += 1;
				}
			}
		}
	} catch (_error) {
		return dayStats;
	}

	return dayStats;
};

const buildDatasetFromDays = (
	label: string,
	dates: Date[],
	dayStats: Map<string, GitDayStats>,
): ActivityDataset => ({
	label,
	points: dates.map((date) => {
		const dayKey = formatDayKey(date);
		const stats = dayStats.get(dayKey) || { publish: 0, update: 0, delete: 0 };

		return {
			label: `${`${date.getMonth() + 1}`.padStart(2, "0")}/${`${date.getDate()}`.padStart(2, "0")}`,
			publish: stats.publish,
			update: stats.update,
			delete: stats.delete,
		};
	}),
});

const buildDatasetFromMonths = (
	label: string,
	dates: Date[],
	dayStats: Map<string, GitDayStats>,
): ActivityDataset => {
	const monthStats = new Map<string, GitDayStats>();

	for (const [dayKey, stats] of dayStats.entries()) {
		const monthKey = dayKey.slice(0, 7);
		const current = monthStats.get(monthKey) || { publish: 0, update: 0, delete: 0 };
		current.publish += stats.publish;
		current.update += stats.update;
		current.delete += stats.delete;
		monthStats.set(monthKey, current);
	}

	return {
		label,
		points: dates.map((date) => {
			const monthKey = `${date.getFullYear()}-${`${date.getMonth() + 1}`.padStart(2, "0")}`;
			const stats = monthStats.get(monthKey) || { publish: 0, update: 0, delete: 0 };

			return {
				label: `${date.getMonth() + 1}月`,
				publish: stats.publish,
				update: stats.update,
				delete: stats.delete,
			};
		}),
	};
};

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

	const recentUpdates = allEntries.slice(0, 5).map((entry) => ({
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

	const dayStats = parseGitActivity();
	const now = new Date();

	return {
		chartDatasets: {
			week: buildDatasetFromDays("近 7 天", createDaySeries(7, now), dayStats),
			month: buildDatasetFromDays("近 30 天", createDaySeries(30, now), dayStats),
			year: buildDatasetFromMonths("近 12 个月", createMonthSeries(12, now), dayStats),
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
