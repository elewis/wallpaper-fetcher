wallpaper-fetcher
=================

Downloads highly rated posts from the 'wallpapers' subreddit and sets them as the desktop background (for people using GNOME3).

## Cron

Running the script in a crontab requires a couple of additional configurations for gsettings. My cron entry is below (times are adjustable, the script will automatically skip wallpaper entries that were downloaded previously).

To run in a crontab, run 'crontab -e' in your shell and insert this line at the bottom of the file (see http://unixhelp.ed.ac.uk/CGI/man-cgi?crontab+5). This example will run the script every six hours:

    0 */6 * * * DISPLAY=:0 GSETTINGS_BACKEND=dconf <SCRIPT LOCATION>


## Dependencies (install via pip)

- requests
- praw (Python Reddit API Wrapper)
- BeautifulSoup