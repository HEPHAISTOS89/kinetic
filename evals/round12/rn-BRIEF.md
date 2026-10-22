# Brief — "Stall" (a Saturday street market, for traders)

Stall is the app for the 120 traders of one weekly street market that runs every
Saturday along a closed high street: food, produce, crafts, second-hand. It is run
by a small market office (two officers and a team of porters). Traders open it during
the week ("have I got my pitch on Saturday? which pitch? can I bring the van in?
will it rain?"), on Saturday morning before 07:00 (load-in window, where to park,
the porters, pitch problems), during the day (footfall, the office's messages, a
neighbour's gazebo in the wind) and after (pay the pitch fee, book next weeks).
Some have traded there for 30 years; some are new. The tone is practical, quick and
sociable — never a sales dashboard, never a gig-economy app.

Design and implement the **home screen** of the app in **React Native** (iOS and
Android). The interface language is **English**.

Data you can assume (use realistic fake data in the gallery only — clearly fixture data):
- the trader (name, business, category, their regular pitch number and size, their
  vehicle, licence and insurance expiry, fees paid and due, bookings for the coming
  weeks);
- the market (this Saturday's layout and pitch allocations, load-in times by zone,
  road-closure times, the weather and wind warnings for gazebos, the office's signed
  messages, the porters on duty, footfall today compared with last week, events
  that change the layout — a parade, roadworks);
- states: an ordinary week with Saturday's pitch confirmed; Saturday 06:30 at load-in
  (zone B, van access until 07:15); pitch moved this week because of roadworks (new
  pitch, why, for how long); high wind warning (gazebo weights required, possible
  early close); the fee for last month overdue; insurance expiring in 10 days (no
  pitch without it); a new trader's first Saturday (where to unload, who to ask,
  the rules); the market cancelled (a storm), with what happens to the fee.
