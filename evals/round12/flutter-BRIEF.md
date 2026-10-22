# Brief — "Col" (a staffed mountain hut)

Col is the app of one staffed mountain hut at 2,480 m, open June to September:
46 bunks in five dormitories, a dining room, a drying room, two wardens and a cook.
Walkers and climbers book a bunk and half-board, then open the app the day before
and on the way up ("is my bunk confirmed? what's the weather on the col tomorrow? is
the path from the valley open? what time is dinner?"), at the hut (check in, which
dormitory, breakfast time for an early start), and when plans change (a storm, a
closed path, a cancellation, a later arrival). Guests range from families on their
first hut night to mountaineers leaving at 4am. The tone is sturdy, exact and
convivial — never an adventure-travel brochure, never a hotel booking app.

Design and implement the **home screen** of the app in **Flutter** (Android and iOS).

Data you can assume (use realistic fake data in the gallery only — clearly fixture data):
- the guest (name, party size, their booking: nights, bunks, half-board, dietary
  needs, deposit paid), the route they plan (from which valley, expected arrival);
- the hut (wardens on duty and their signed notes, dinner and breakfast times, early
  breakfast for alpinists, beds left tonight, the drying room, water and showers),
  the mountain (forecast for the col and the summit, freezing level, avalanche or
  rockfall notices, path conditions from each valley, the last safe departure time
  from the valley);
- states: the day before a booked night; on the way up (expected arrival 17:30,
  dinner at 19:00); arrived and checked in (dormitory 3, bunks 12–13); a storm
  forecast for tomorrow (the wardens advise staying a second night or descending
  early); the path from one valley closed by rockfall (the other path, extra time);
  the hut full tonight (waitlist, the nearest other hut); a late arrival after
  the last safe departure time; a family's first hut night (what to bring, hut
  rules, quiet hours).
