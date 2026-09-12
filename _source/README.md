# Edward R. Morrison, personal website

Jekyll site published by GitHub Pages. Live at https://edwardrmorrison.com

The look is Ed's existing site, unchanged: `styles.css` is byte-identical to the
original and the page markup matches it. What changed is underneath. The header,
photo and menu are now written once in `_layouts/default.html` instead of being
copy-pasted into all five pages, and the papers are data instead of hand-written
HTML.

## How to add a published paper

Open `_data/publications.yml` and add a block at the top. Nothing else changes.

```yaml
- title: "Title of the paper"
  url: "https://link-to-the-paper"
  year: 2026
  journal: "Journal of Legal Studies"
  volume: "45(2)"
  coauthors:
    - name: "Coauthor Name"
      url: "https://their-page"     # optional
```

Book chapter, use `book` instead of `journal`:

```yaml
- title: "Title of the chapter"
  url: "https://link"
  year: 2026
  book: "Title of the Book"
  book_url: "https://link-to-the-book"   # optional
  book_note: "(Publisher: Editor, ed., 2026)"
```

Press or anything else, use `outlet: "Law360.com (June 9, 2026)"`.

Papers appear in file order, newest first, which is how the list already reads.
Put a new paper at the top.

Working papers live in `_data/working_papers.yml` and use `status:` ("in draft",
"in progress", "available on SSRN") in place of a year.

## To change Ed's titles, photo, email or CV

All of it is in `_data/profile.yml`. Editing it updates every page at once.

## Books and amicus briefs

Short lists, written directly in `books.html` and `amicusbriefs.html`.

## How it publishes

GitHub Pages builds Jekyll automatically. Push to `main` and the live site
updates in a minute or two. There is no build step to run and no GitHub Action
to maintain.

Editing a file in the GitHub web editor and clicking "Commit changes" is enough.

## Files

| File | What it is |
|---|---|
| `_layouts/default.html` | The page frame: header, photo, menu. Written once |
| `_data/profile.yml` | Name, titles, photo, email, CV link |
| `_data/publications.yml` | Published papers, as data |
| `_data/working_papers.yml` | Working papers, as data |
| `_data/nav.yml` | The menu |
| `_includes/coauthors.html` | Formats "With A, B, and C". Should not need editing |
| `styles.css` | The original stylesheet, unchanged |
| `CNAME` | The custom domain. Deleting it breaks edwardrmorrison.com |

## The original site is kept, not discarded

`_archive/original-2021/` holds a byte copy of Ed's site as it stood on
2021-11-29, and `edmorrisonportraittemp.jpg` is still at the repo root so any
old link to the previous photo still resolves. Neither is published. They exist
so the before/after can be rebuilt without depending on the old `ssh2192`
account staying reachable.
