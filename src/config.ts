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
	footer: {
		visitorCounterApi: "https://busuanzi.9420.ltd/js",
	},
	backgroundMusic: {
		enable: true,
		title: "音乐",
		autoplay: false,
		loop: true,
		defaultTrackId: "cold-orbit",
		tracks: [
			{
				id: "cold-orbit",
				title: "Cold Orbit",
				artist: "AlexGrohl",
				group: "dark-ambient",
				src: "/audio/background/cold-orbit.mp3",
			},
			{
				id: "secret-motive",
				title: "Secret Motive",
				artist: "AlexGrohl",
				group: "dark-piano",
				src: "/audio/background/secret-motive.mp3",
			},
			{
				id: "ambient-space-background",
				title: "Ambient Space Background",
				artist: "Universfield",
				group: "space-ambient",
				src: "/audio/background/ambient-space-background.mp3",
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
			name: "总览",
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
	bio: "记录正在发生的思考，也记录正在成形的作品。",
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
