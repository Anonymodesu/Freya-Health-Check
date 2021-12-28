This contains some short Selenium code to automate checking whether https://bmvs.onlineappointmentscheduling.net.au/oasis/Default.aspx has an available booking.

Run the following commands:

```
py -m venv .venv
.\.venv\Scripts\activate.bat
pip install -r .\requirements.txt
py .\check_availability.py
```