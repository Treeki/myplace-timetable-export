Strath MyPlace ICS Generator
============================

This is a pair of Python scripts for exporting class timetables from the
University of Strathclyde MyPlace service to iCalendar subscription files.

Written using Python 3. Depends on the following modules from PyPI: `requests`,
`icalendar`

`fetcher.py` uses the internal API used by the Strathclyde mobile app to fetch
the class timetable and save it to `calendar.json`, using the authentication
credentials specified in `config.json`.

`parser.py` reads `calendar.json` and generates `calendar.ics`.

The easiest way to fetch the authentication credentials for `config.json` is
to set up some sort of proxy (like mitmproxy, Fiddler or Charles) on your
machine and then capture one of the requests made by the app. The required
token ID and device ID can be extracted from the HTTP headers.

The app uses SSL but does not pin certificates so no modification is required.

Class timetables at Strathclyde can sometimes change with little warning
(especially room assignments and the first few weeks of the semester), so it
may be a good idea to run these scripts a couple of times a day using cron.
