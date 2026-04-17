import { execSync } from "node:child_process";
import { type CollectionEntry, getCollection } from "astro:content";
import { getCategoryList } from "./content-utils";

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
};

type DashboardPostSummary = {
	title: string;
	url: string;
	excerpt: string;
};

type DashboardMetrics = {
	updatedPosts: number;
	updatedWords: number;
	totalUsage: string;
	totalUsageNote: string;
	lastVisitedPost: DashboardPostSummary;
	latestPost: DashboardPostSummary;
};

type DashboardData = {
	chartDatasets: Record<"week" | "month" | "year", ActivityDataset>;
	recentUpdates: DashboardRecentUpdate[];
	dashboardMetrics: DashboardMetrics;
};

type PostEntry = CollectionEntry<"posts"> & {
	body: string;
};

type GitDayStats = {
	publish: number;
	update: number;
	delete: number;
};

const DASHBOARD_FALLBACK_POST: DashboardPostSummary = {
	title: "暂无文章",
	url: "/archive/",
	excerpt: "当前还没有可用于展示的文章数据。",
};

const isMarkdownPostPath = (filePath: string) =>
	/\.md$/i.test(filePath) &&
	(filePath.includes("src/content/posts/") || filePath.includes("src\\content\\posts\\"));

const formatDateTime = (date: Date) =>
	new Intl.DateTimeFormat("zh-CN", {
		year: "numeric",
		month: "2-digit",
		day: "2-digit",
		hour: "2-digit",
		minute: "2-digit",
		hour12: false,
	}).format(date);

const formatPostUrl = (slug: string) => `/posts/${slug}/`;

const toPostSummary = (post?: PostEntry): DashboardPostSummary => {
	if (!post) {
		return DASHBOARD_FALLBACK_POST;
	}

	return {
		title: post.data.title,
		url: formatPostUrl(post.slug),
		excerpt: post.data.description || "这篇文章暂时还没有补充摘要。",
	};
};

const getWordCount = (content: string) => {
	const latinWords = content.match(/[A-Za-z0-9_]+/g)?.length ?? 0;
	const cjkChars = content.match(/[\u3400-\u9fff]/g)?.length ?? 0;
	return latinWords + cjkChars;
};

const getPostDisplayDate = (post: PostEntry) =>
	new Date(post.data.updated ?? post.data.published);

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
			'git log --name-status --find-renames --date=short --format="commit %H %ad" -- src/content/posts',
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
				if (isMarkdownPostPath(filePath)) {
					stats.publish += 1;
				}
				continue;
			}

			if (status.startsWith("M")) {
				const filePath = parts[1] || "";
				if (isMarkdownPostPath(filePath)) {
					stats.update += 1;
				}
				continue;
			}

			if (status.startsWith("D")) {
				const filePath = parts[1] || "";
				if (isMarkdownPostPath(filePath)) {
					stats.delete += 1;
				}
				continue;
			}

			if (status.startsWith("R") || status.startsWith("C")) {
				const targetPath = parts[2] || parts[1] || "";
				if (isMarkdownPostPath(targetPath)) {
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
			const stats = monthStats.get(monthKey) || {
				publish: 0,
				update: 0,
				delete: 0,
			};

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
	const posts = (await getCollection("posts", ({ data }) => {
		return import.meta.env.PROD ? data.draft !== true : true;
	})) as PostEntry[];
	const categories = await getCategoryList();

	const postsByUpdated = [...posts].sort(
		(a, b) => getPostDisplayDate(b).getTime() - getPostDisplayDate(a).getTime(),
	);
	const postsByPublished = [...posts].sort(
		(a, b) =>
			new Date(b.data.published).getTime() - new Date(a.data.published).getTime(),
	);

	const thirtyDaysAgo = startOfDay(new Date());
	thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 29);

	const updatedPosts = posts.filter(
		(post) => getPostDisplayDate(post).getTime() >= thirtyDaysAgo.getTime(),
	);

	const updatedWords = updatedPosts.reduce(
		(sum, post) => sum + getWordCount(post.body || ""),
		0,
	);

	const recentUpdates = postsByUpdated.slice(0, 3).map((post) => ({
		title: post.data.title,
		time: formatDateTime(getPostDisplayDate(post)),
		url: formatPostUrl(post.slug),
		description: post.data.description || "这篇文章暂时还没有补充摘要。",
	}));

	const categorySummary = categories
		.slice(0, 3)
		.map((category) => `${category.name} ${category.count} 篇`)
		.join("，");

	const dayStats = parseGitActivity();
	const now = new Date();

	return {
		chartDatasets: {
			week: buildDatasetFromDays("近7日", createDaySeries(7, now), dayStats),
			month: buildDatasetFromDays("近1个月", createDaySeries(30, now), dayStats),
			year: buildDatasetFromMonths("近1年", createMonthSeries(12, now), dayStats),
		},
		recentUpdates,
		dashboardMetrics: {
			updatedPosts: updatedPosts.length,
			updatedWords,
			totalUsage: `${categories.length} 个分类`,
			totalUsageNote: `当前共 ${posts.length} 篇文章${categorySummary ? `，${categorySummary}` : ""}`,
			lastVisitedPost: toPostSummary(postsByUpdated[0]),
			latestPost: toPostSummary(postsByPublished[0]),
		},
	};
}
