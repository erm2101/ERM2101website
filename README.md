# Edward R. Morrison, personal website

Live at https://edwardrmorrison.com, hosted on GoDaddy.

Everything in the top level of this repository is the website itself: plain HTML, CSS,
one small JavaScript file, the portrait and the CVs. There is nothing to build on the
server and nothing to install. GoDaddy shared hosting serves Apache only, so the pages
here are already compiled.

The Jekyll source the site is generated from is kept in `_source/`. It is not part of
the website and is not uploaded.

## Uploading to GoDaddy

1. In GoDaddy, open **cPanel > File Manager** and go to `public_html`.
2. Upload every file and folder from the top level of this repository **except**
   `_source/` and `README.md`.
3. Make sure `.htaccess` came across. File Manager hides dotfiles by default:
   **Settings > Show Hidden Files (dotfiles)**.
4. Visit the domain. `index.html` is served automatically at the root.

To upload in one step instead, download this repository as a ZIP, delete `_source/`
and `README.md` from it, then use File Manager's **Upload** and **Extract** on the
remaining ZIP.

### Turning on HTTPS

Do this in GoDaddy, not in `.htaccess`: **cPanel > Security > SSL/TLS Status**, install
the certificate for the domain, then switch on **Force HTTPS Redirect**. The redirect is
deliberately not in `.htaccess`, because doing it there can loop behind GoDaddy's proxy.

### Pointing the domain at the hosting

GitHub Pages used to handle two things that GoDaddy now handles in DNS, so both need
checking once after the first upload:

| Was handled by | Now set in |
|---|---|
| The `CNAME` file, which tied the domain to the site | GoDaddy **Domains > DNS**: the A record for `@` points at the hosting IP |
| GitHub redirecting `www.edwardrmorrison.com` to the apex | GoDaddy DNS: a `CNAME` record for `www` pointing at `edwardrmorrison.com` |

Without the second one, `www.edwardrmorrison.com` will not resolve even though the bare
domain does.

## Changing the content

Content lives as data in `_source/`, not in the HTML. Edit the relevant file there, then
rebuild.

| To change | Edit |
|---|---|
| A published paper | `_source/_data/publications.yml` |
| A working paper | `_source/_data/working_papers.yml` |
| Name, titles, photo, email, CV link | `_source/_data/profile.yml` |
| The menu | `_source/_data/nav.yml` |
| Books, amicus briefs | `_source/books.html`, `_source/amicusbriefs.html` |
| The page frame, header, photo | `_source/_layouts/default.html` |
| The look | `styles.css` at the top level |

Papers appear in file order, newest first. Put a new one at the top.

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

For a book chapter use `book:` in place of `journal:`, with optional `book_url:` and
`book_note:`. For press or anything else use `outlet: "Law360.com (June 9, 2026)"`.
Working papers take `status:` ("in draft", "in progress", "available on SSRN") instead
of a year.

### Rebuilding

```
pip install python-liquid pyyaml
python3 _source/build.py
```

That rewrites the HTML at the top level, regenerates `404.html` from the same layout,
and leaves `.htaccess` alone. Re-upload the files that changed.

The build is deterministic: running it twice on unchanged source produces byte-identical
output, so `git status` after a rebuild shows exactly what your edit changed and nothing
else.

## Files

| File | What it is |
|---|---|
| `index.html` and the four other pages | The site. Compiled, do not hand-edit, they are overwritten on rebuild |
| `404.html` | Page-not-found, generated from the same layout so it always matches |
| `styles.css` | Ed's original stylesheet |
| `scale.fix.js` | Viewport fix for iPhone, from the original site |
| `.htaccess` | Apache settings: default page, 404, UTF-8, no directory listings |
| `edmorrisonportrait.jpg` | The portrait |
| `edward_morrison_cv_aug_2026.pdf` | The current CV, linked from the home page |
| Older CV PDFs, `edmorrisonportraittemp.jpg` | Kept so older links to them still resolve |
| `_source/` | The Jekyll source and `build.py`. Not part of the website |
| `_source/_archive/original-2021/` | Ed's site as it stood on 2021-11-29, kept for reference |

## Note on GitHub Pages

This site used to be set up for GitHub Pages, which builds Jekyll automatically. GoDaddy
does not, which is why the HTML is compiled here instead. The `CNAME` file that GitHub
Pages needed is kept in `_source/` but has no effect on GoDaddy; the domain is pointed at
the host through GoDaddy's own DNS.
