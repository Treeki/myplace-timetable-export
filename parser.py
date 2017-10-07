import icalendar
import json
import pytz
from datetime import date,time,datetime,timedelta

def parse_date(string):
	y, m, d = string.split('-')
	return date(int(y), int(m), int(d))

def parse_time(string, tzinfo):
	h, m = string.split(':')
	return time(int(h), int(m), tzinfo=tzinfo)

def nice_type(activity_type):
	if activity_type == 'Computer Lab':
		return 'Lab'
	else:
		return activity_type

def nice_location(name, desc):
	if desc.startswith('Room ') and name in BUILDING_CODES:
		number = desc[5:]
		number = number[:number.index(',')]
		return BUILDING_CODES[name] + number
	else:
		return name + ' | ' + desc

BUILDING_CODES = {
	'181 St James Road': 'EM',
	'Alexander Turnbull Building': 'AT',
	'Andrew Ure Hall': 'AU',
	'Architecture Building': 'AR',
	'Barony Hall': 'BH',
	'Birkbeck Court': 'BC',
	"Chancellor's Hall": 'CH',
	'Collins Building': 'CL',
	'Colville Building': 'CV',
	'Curran Building': 'CU',
	'Forbes Hall': 'FH',
	'Garnett Hall': 'GA',
	'Graham Hills Building': 'GH',
	'Hamnett Wing': 'HW',
	'Henry Dyer Building': 'HD',
	'James Blyth Court': 'JB',
	'James Goold Hall': 'JG',
	'James Weir Building': 'JW',
	'James Young Hall': 'JY',
	'John Anderson Building': 'JA',
	'Livingstone Tower': 'LT',
	'Lord Hope Building': 'LH',
	'Lord Todd': 'LD',
	'McCance Building': 'MC',
	'Murray Hall': 'MH',
	'Patrick Thomas Court': 'PT',
	'Ramshorn Theatre': 'RT',
	'Robertson Wing': 'AB',
	'Royal College Building': 'RC',
	'Sir William Duncan Building': 'WD',
	'St Pauls Chaplaincy Centre': 'SP',
	'Stenhouse Building': 'ST',
	'Stenhouse Wing': 'ST',
	'Strathclyde Business School': 'SB',
	"Students' Union": 'SU',
	'Thomas Campbell Court': 'TC',
	'Thomas Graham Building': 'TG',
	'University Centre': 'UC',
	'Wolfson Building': 'WC'
}

cal = icalendar.Calendar()
cal.add('prodid', '-//Stuff//Strath MyPlace ICS Generator//EN')
cal.add('version', '2.0')
cal.add('x-apple-calendar-color', '#7A81FF')

tz = pytz.timezone('Europe/London')

with open('calendar.json', 'r') as f:
	blob = json.load(f)

for week in blob['data']['weeks']:
	current_date = parse_date(week['weekStart'])
	generic_dtstamp = datetime.combine(current_date, time())

	for day in week['days']:
		for activity in day['activities']:
			class_code = '/'.join([c['classCode'] for c in activity['classes']])
			title = '%s %s' % (class_code, nice_type(activity['activityType']))

			start_time = parse_time(activity['startTime'], tz)
			start_stamp = datetime.combine(current_date, start_time)
			end_time = parse_time(activity['endTime'], tz)
			end_stamp = datetime.combine(current_date, end_time)

			event = icalendar.Event()
			event.add('summary', title)
			event.add('dtstart', start_stamp)
			event.add('dtend', end_stamp)
			event.add('dtstamp', generic_dtstamp)
			event.add('location', nice_location(activity['location'], activity['locationDesc']))

			cal.add_component(event)

		current_date += timedelta(days=1)

with open('calendar.ics', 'wb') as f:
	f.write(cal.to_ical())

