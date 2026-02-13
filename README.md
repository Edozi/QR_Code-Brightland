BRIGHTLAND CONCERT QR TICKETING SYSTEM
A secure QR-based concert ticket validation system built with:
1. FastAPI (Backend API)
2. Supabase (PostgreSQL) (Database)
3. Vercel (Frontend Deployment)
4. UUID-based Secure Tickets
5. QR Code Entry Scanning System


------  OVERVIEW  ------
This system generates secure QR tickets for event entry and validates them in real-time at the gate.
Each ticket includes:
1. UUID (Secure Identifier) – Used for validation
2. Public Ticket Number (Serial Format) – For planners & tracking
3. Scanner Tracking
4. Usage Timestamp
5. Status (valid / used)
The system prevents duplication by validating tickets against the database and marking them as used upon successful scan.



------  SYSTEM ARCHITECTURE  ------
Ticket Security Model
Each ticket contains:
| Field           | Purpose                                          |
| --------------- | ------------------------------------------------ |
| `id (UUID)`     | Secure identifier embedded in QR                 |
| `sequence_id`   | Auto-increment internal counter                  |
| `public_number` | Human-readable number (e.g., Concert-2024-00001) |
| `status`        | `valid` or `used`                                |
| `used_at`       | Timestamp of scan                                |
| `scanner_id`    | Device/staff identifier                          |

Important:
The QR code contains only the UUID. The public ticket number is NOT used for authentication. Validation is performed strictly using the UUID


------  DATABASE STRUCTURE (Supabase / PostgreSQL)  ------
Using the SQL Editor
    CREATE TABLE concert_tickets (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        sequence_id BIGSERIAL UNIQUE,
        public_number TEXT UNIQUE,
        status TEXT DEFAULT 'valid',
        used_at TIMESTAMP NULL,
        scanner_id TEXT NULL,

        created_at TIMESTAMP DEFAULT NOW()
    );


------  TICKET VERIFICATION FLOW  ------
1. Scanner reads QR
2. Extracts UUID from URL
3. Sends UUID to backend /verify
4. Backend:
    a. Checks if ticket exists
    b. Checks if status = valid
    c. Marks ticket as used
    d. Records used_at
    e. Records scanner_id
5. Returns response
If already used → rejected.


------ ANTI-DUPLICATION MEASURES  ------
1. UUID-based validation (unguessable)
2. Database verification
3. Status-based locking
4. Timestamp logging
5. Scanner device tracking
Even if someone guesses public ticket numbers, entry is impossible without a valid UUID.