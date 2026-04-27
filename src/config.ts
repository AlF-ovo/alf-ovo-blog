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
	subtitle: "记录 Pwn、CTF 与零散思考的小站。",
	lang: "zh_CN",
	themeColor: {
		hue: 250,
		fixed: false,
	},
	banner: {
		enable: false,
		src: "assets/images/demo-banner.png",
		position: "center",
		credit: {
			enable: false,
			text: "",
			url: "",
		},
	},
	toc: {
		enable: true,
		depth: 2,
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
				title: "Music 1 / Part 01",
				artist: "EV Music 1",
				group: "music-1",
				src: "/audio/background/ev-music-1-part-01.m4a",
			},
			{
				id: "ev-music-2-part-01",
				title: "Music 2 / Part 01",
				artist: "EV Music 2",
				group: "music-2",
				src: "/audio/background/ev-music-2-part-01.m4a",
			},
			{
				id: "ev-music-1-part-02",
				title: "Music 1 / Part 02",
				artist: "EV Music 1",
				group: "music-1",
				src: "/audio/background/ev-music-1-part-02.m4a",
			},
			{
				id: "ev-music-2-part-02",
				title: "Music 2 / Part 02",
				artist: "EV Music 2",
				group: "music-2",
				src: "/audio/background/ev-music-2-part-02.m4a",
			},
			{
				id: "ev-music-1-part-03",
				title: "Music 1 / Part 03",
				artist: "EV Music 1",
				group: "music-1",
				src: "/audio/background/ev-music-1-part-03.m4a",
			},
			{
				id: "ev-music-2-part-03",
				title: "Music 2 / Part 03",
				artist: "EV Music 2",
				group: "music-2",
				src: "/audio/background/ev-music-2-part-03.m4a",
			},
			{
				id: "ev-music-2-part-04",
				title: "Music 2 / Part 04",
				artist: "EV Music 2",
				group: "music-2",
				src: "/audio/background/ev-music-2-part-04.m4a",
			},
		],
	},
	favicon: [],
};

export const navBarConfig: NavBarConfig = {
	links: [
		LinkPreset.Home,
		{
			name: "札记",
			url: "/notes/",
		},
		LinkPreset.Archive,
		{
			name: "友链",
			url: "/links/",
		},
		LinkPreset.About,
		{
			name: "Dashboard",
			url: "/dashboard/",
		},
		{
			name: "GitHub",
			url: "https://github.com/AlF-ovo/alf-ovo-blog",
			external: true,
		},
	],
};

export const profileConfig: ProfileConfig = {
	avatar: "assets/images/alf-avatar.png",
	name: "AlF",
	bio: "哥先走了，有事受着",
	quote: "在终端、断点和未写完的笔记之间继续前进。",
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
	theme: "github-dark",
};
