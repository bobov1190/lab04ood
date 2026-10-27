# Task 3 - dental clinic booking (paper task, so only text here)
#
# 3.1 Nouns and verbs
#   verbs: books, works, moved, charged, confirms, sends
#
#   class:      Patient, Appointment, Dentist, Procedure, TreatmentRoom
#   attribute:  name, duration, price (of Procedure), working hours (of Dentist),
#               start time (of Appointment), status
#   actor:      receptionist, system
#   event with data: Appointment (patient + dentist + procedure + time),
#               SMS reminder
#   vague word (must ask): "moved" (how many times? can the patient choose any
#               time?), "24 hours before" (before the old start or the new one?),
#               "evening before" (which hour? which time zone?),
#               "confirms" (is an unconfirmed appointment already booked?),
#               "fee is charged" (when and how does the patient pay?),
#               "one room" (is the room always the same?)
#
# 3.2 CRC cards
#
#   Appointment
#     - knows patient, dentist, procedure, start time and status
#     - knows its end time (start + procedure duration)
#     - calculates the reschedule fee (free until 24h, then 50 000)
#     - moves to a new time and gets confirmed
#     collaborators: Patient, Dentist, Procedure, Receptionist
#
#   Dentist
#     - knows his room and working hours
#     - checks that a time slot is inside working hours
#     - checks that he is not booked twice at the same time
#     - keeps his list of appointments
#     collaborators: Appointment, TreatmentRoom
#
#   Procedure
#     - knows name, duration and price
#     collaborators: none
#
#   Patient
#     - knows name and phone number
#     collaborators: none
#
#   ReminderService
#     - finds appointments that start tomorrow
#     - makes the text of the reminder
#     - gives the text to the SMS client
#     collaborators: Appointment, Patient, SmsClient
#
# 3.3 Double booking is checked by Dentist, because the dentist is the one
#     who has the list of all his appointments and his working hours. One
#     Appointment knows only itself and can not see the others.
#     The 50 000 fee is calculated by Appointment, because it has the start
#     time (it only needs "now" from outside) and it is the thing that is moved.
#
# 3.4 Yes it changes. Receptionist is no longer just an actor, we must store who
#     confirmed. So Receptionist becomes a class (card with name/id, he calls
#     confirm). On the Appointment card we add confirmed_by and confirmed_at,
#     confirm(receptionist) saves them, and Receptionist is a new collaborator.
#     Now we have 6 cards.
#
# 3.5 No. Appointment knows nothing about phones and SMS providers, if it sends
#     SMS it has two jobs and it is hard to test. ReminderService sends it.
#     Relationship between them: dependency (ReminderService only uses
#     Appointment objects that it gets as a parameter, it does not store them).
