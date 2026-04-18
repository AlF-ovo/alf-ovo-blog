import type {
	ExpressiveCodeConfig,
	LicenseConfig,
	NavBarConfig,
	ProfileConfig,
	SiteConfig,
} from "./types/config";
import { LinkPreset } from "./types/config";

export const siteConfig: SiteConfig = {
	title: "AlF-ovo's Blog",
	subtitle: "\u6b22\u8fce\u4f60\u6765\u6211\u7684\u535a\u5ba2\u73a9:)",
	lang: "zh_CN", // Language code, e.g. 'en', 'zh_CN', 'ja', etc.
	themeColor: {
		hue: 250, // Default hue for the theme color, from 0 to 360. e.g. red: 0, teal: 200, cyan: 250, pink: 345
		fixed: false, // Hide the theme color picker for visitors
	},
	banner: {
		enable: false,
		src: "assets/images/demo-banner.png", // Relative to the /src directory. Relative to the /public directory if it starts with '/'
		position: "center", // Equivalent to object-position, only supports 'top', 'center', 'bottom'. 'center' by default
		credit: {
			enable: false, // Display the credit text of the banner image
			text: "", // Credit text to be displayed
			url: "", // (Optional) URL link to the original artwork or artist's page
		},
	},
	toc: {
		enable: true, // Display the table of contents on the right side of the post
		depth: 2, // Maximum heading depth to show in the table, from 1 to 3
	},
	backgroundMusic: {
		enable: true,
		title: "Music",
		autoplay: false,
		loop: true,
		defaultTrackId: "ev-music-1-part-01",
		tracks: [
			{
				id: "ev-music-1-part-01",
				title: "音乐 1 · 片段 01",
				artist: "EV录屏 音乐1",
				group: "music-1",
				src: "/audio/background/ev-music-1-part-01.m4a",
			},
			{
				id: "ev-music-2-part-01",
				title: "音乐 2 · 片段 01",
				artist: "EV录屏 音乐2",
				group: "music-2",
				src: "/audio/background/ev-music-2-part-01.m4a",
			},
			{
				id: "ev-music-1-part-02",
				title: "音乐 1 · 片段 02",
				artist: "EV录屏 音乐1",
				group: "music-1",
				src: "/audio/background/ev-music-1-part-02.m4a",
			},
			{
				id: "ev-music-2-part-02",
				title: "音乐 2 · 片段 02",
				artist: "EV录屏 音乐2",
				group: "music-2",
				src: "/audio/background/ev-music-2-part-02.m4a",
			},
			{
				id: "ev-music-1-part-03",
				title: "音乐 1 · 片段 03",
				artist: "EV录屏 音乐1",
				group: "music-1",
				src: "/audio/background/ev-music-1-part-03.m4a",
			},
			{
				id: "ev-music-2-part-03",
				title: "音乐 2 · 片段 03",
				artist: "EV录屏 音乐2",
				group: "music-2",
				src: "/audio/background/ev-music-2-part-03.m4a",
			},
			{
				id: "ev-music-2-part-04",
				title: "音乐 2 · 片段 04",
				artist: "EV录屏 音乐2",
				group: "music-2",
				src: "/audio/background/ev-music-2-part-04.m4a",
			},
		],
	},
	favicon: [
		// Leave this array empty to use the default favicon
		// {
		//   src: '/favicon/icon.png',    // Path of the favicon, relative to the /public directory
		//   theme: 'light',              // (Optional) Either 'light' or 'dark', set only if you have different favicons for light and dark mode
		//   sizes: '32x32',              // (Optional) Size of the favicon, set only if you have favicons of different sizes
		// }
	],
};

export const navBarConfig: NavBarConfig = {
	links: [
		LinkPreset.Home,
		{
			name: "\u624e\u8bb0",
			url: "/notes/",
		},
		LinkPreset.Archive,
		{
			name: "\u53cb\u94fe",
			url: "/links/",
		},
		LinkPreset.About,
		{
			name: "Dashboard",
			url: "/dashboard/",
		},
		{
			name: "GitHub",
			url: "https://github.com/AlF-ovo/alf-ovo-blog", // Internal links should not include the base path, as it is automatically added
			external: true, // Show an external link icon and will open in a new tab
		},
	],
};

export const profileConfig: ProfileConfig = {
	avatar: "assets/images/alf-avatar.png", // Relative to the /src directory. Relative to the /public directory if it starts with '/'
	name: "AlF",
	bio: "\u54e5\u5148\u8d70\u4e86\uff0c\u6709\u4e8b\u53d7\u7740",
	quote: "Between terminals, breakpoints, and unfinished notes.",
	links: [
		{
			name: "GitHub",
			icon: "fa6-brands:github",
			url: "https://github.com/AlF-ovo/alf-ovo-blog",
		},
	],
};

export const licenseConfig: LicenseConfig = {
	enable: true,
	name: "CC BY-NC-SA 4.0",
	url: "https://creativecommons.org/licenses/by-nc-sa/4.0/",
};

export const expressiveCodeConfig: ExpressiveCodeConfig = {
	// Note: Some styles (such as background color) are being overridden, see the astro.config.mjs file.
	// Please select a dark theme, as this blog theme currently only supports dark background color
	theme: "github-dark",
};
