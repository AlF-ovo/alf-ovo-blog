import { defineCollection, z } from "astro:content";

const contentEntrySchema = z.object({
	title: z.string(),
	published: z.date(),
	updated: z.date().optional(),
	draft: z.boolean().optional().default(false),
	description: z.string().optional().default(""),
	image: z.string().optional().default(""),
	tags: z.array(z.string()).optional().default([]),
	category: z.string().optional().nullable().default(""),
	categoryPath: z.array(z.string()).optional().default([]),
	series: z.string().optional().default(""),
	lang: z.string().optional().default(""),

	/* For internal use */
	prevTitle: z.string().default(""),
	prevSlug: z.string().default(""),
	nextTitle: z.string().default(""),
	nextSlug: z.string().default(""),
});

const postsCollection = defineCollection({
	schema: contentEntrySchema,
});

const notesCollection = defineCollection({
	schema: contentEntrySchema,
});
const specCollection = defineCollection({
	schema: z.object({}),
});
export const collections = {
	posts: postsCollection,
	notes: notesCollection,
	spec: specCollection,
};
