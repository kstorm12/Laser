# Windows laser PC: setup and daily use

The Windows PC that drives the laser (EzCad2, and LightBurn once licensed) keeps a git clone of
this repo at `C:\Laser`. It pulls settings and art from GitHub, and pushes back what it makes:
saved job files (`.ezd`, `.lbrn2`) and photos. Omarchy and the PC are both writers, so each one
pulls before it edits.

The repo is **public**: anything pushed from the PC (photos, job files) is visible to anyone.

## One-time setup

1. Install Git for Windows. **PowerShell (laser PC), any directory:**

   ```powershell
   winget install --id Git.Git -e
   ```

   Close and reopen PowerShell so `git` is on the PATH.

2. Clone and set your identity. **PowerShell (laser PC), `cd C:\`:**

   ```powershell
   git clone https://github.com/kstorm12/Laser.git C:\Laser
   cd C:\Laser
   git config user.name "kstorm12"
   git config user.email "kstorm0813@gmail.com"
   ```

   Keep the clone at `C:\Laser`: a short path stays clear of the 260-character MAX_PATH limit.

3. First push signs in. The first time `save.bat` pushes, Git Credential Manager (bundled with
   Git for Windows) opens a browser for a GitHub login and remembers it. Pulling needs no login.

4. Pin `update.bat` and `save.bat` to the desktop or taskbar (right-click > Send to > Desktop).

## Daily use

| When | Do |
|---|---|
| Before a job | Double-click `update.bat`. Gets the latest settings, art, and job cards |
| After a job (saved an `.ezd`/`.lbrn2`, took photos) | Copy files into the job's folder under `projects/`, then double-click `save.bat` and type a short note |
| On Omarchy, before editing | `git pull` (the PC may have pushed) |

Where things go:

- Job files: `projects/<category>/<job>/designs/` (e.g. `p790-logo.ezd`, `p790-logo.lbrn2`).
- Cropped photos: `projects/<category>/<job>/photos/`. Raw phone photos go in `photos/raw/`,
  which is gitignored and never pushed.
- Lens correction (`.cor`) and EzCad2 config (`markcfg7`) backups: `machine-config/` (see
  `lightburn.md`). These are the machine's calibration; keep a copy in the repo.

Avoid `&`, `|`, `<`, `>` and `%` in the `save.bat` note: cmd.exe treats them as commands.

## If update fails

`update.bat` only fast-forwards. It refuses when the PC and GitHub have both changed:

- **"Your local changes would be overwritten"**: a file in the repo was edited on the PC and not
  saved. Run `save.bat` first, then `update.bat`.
- **"Not possible to fast-forward"**: both sides committed. **PowerShell (laser PC),
  `cd C:\Laser`:**

  ```powershell
  git pull --rebase
  git push
  ```

  If the rebase stops on a conflict, stop there and fix it from Omarchy rather than guessing:
  binary job files (`.ezd`) cannot be merged, only one side kept.

To avoid conflicts entirely: edit Markdown on Omarchy, save job files and photos on the PC.
