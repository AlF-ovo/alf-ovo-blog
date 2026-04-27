import rss from "@astrojs/rss";
import { getAllSortedContentEntries } from "@utils/content-utils";
import { getCollectionUrl } from "@utils/url-utils";
import type { APIContext } from "astro";
import MarkdownIt from "markdown-it";
import sanitizeHtml from "sanitize-html";
import { siteConfig } from "@/config";

const parser = new MarkdownIt();

function stripInvalidXmlChars(str: string): string {
	return str.replace(
		// biome-ignore lint/suspicious/noControlCharactersInRegex: https://www.w3.org/TR/xml/#charsets
		/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F\uFDD0-\uFDEF\uFFFE\uFFFF]/g,
		"",
	);
}

export async function GET(context: APIContext) {
	const contentEntries = await getAllSortedContentEntries();

	return rss({
		title: siteConfig.title,
		description: siteConfig.subtitle || "No description",
		site: context.site ?? "https://fuwari.vercel.app",
		items: contentEntries.map(({ collection, entry }) => {
			const content = typeof entry.body === "string" ? entry.body : String(entry.body || "");
			const cleanedContent = stripInvalidXmlChars(content);
			return {
				title: entry.data.title,
				pubDate: entry.data.published,
				description: entry.data.description || "",
				link: getCollectionUrl(collection, entry.slug),
				content: sanitizeHtml(parser.render(cleanedContent), {
					allowedTags: sanitizeHtml.defaults.allowedTags.concat(["img"]),
				}),
			};
		}),
		customData: `<language>${siteConfig.lang}</language>`,
	});
}
