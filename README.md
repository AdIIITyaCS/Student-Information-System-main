Goal: 
a Django Student Information System where student registrations are mirrored to MongoDB Atlas while Django/SQLite remains the primary store for admin CRUD and app logic.

Architecture: 
hybrid — Django + SQLite for app behavior and admin; PyMongo writes/registers to student_db.studentCollections for Atlas visibility.

Key pieces: 
main app (models/views/forms), Mongo helper (mongo.py), registration mirroring in forms.py, and admin fallback in views.py.

Deployment on Render:
render-build.sh runs installs, migrate, collectstatic, the sync (sync_mongo_to_sqlite.py) and non-interactive admin creation (create_admin.py). Start with gunicorn student_system.wsgi:application.

Making admin CRUD available on Render: 
run the sync script once (Render Shell or build) to create Django User + StudentProfile records from Mongo documents; afterward /admin-panel/students/ shows full View/Delete actions. 

Command: 
python scripts/sync_mongo_to_sqlite.py (or $PYTHON scripts/sync_mongo_to_sqlite.py).

Important env vars:
set MONGO_URI (URL-encode special chars), MONGO_DB_NAME, MONGO_COLLECTION, ADMIN_USERNAME, ADMIN_PASSWORD, SITE_URL, and SECRET_KEY on Render.

Recent fixes:
removed djongo (incompatible), handled Render Python path issues with ${PYTHON:-python3}, added sys.path fixes for build scripts, replaced make_random_password with get_random_string.

Next steps: 
commit & push latest fixes, run the sync script on the server, set DEBUG=False and move relational DB to managed Postgres for production.
