# Winnow-Solutions---Software-Test-Engineer-Internship


1. Design Description (Documentația)
Arhitectura Sistemului
Sistemul este conceput ca un microserviciu REST API.
•	Interfață: HTTP API (ușor de integrat în orice Test Runner: PyTest, Selenium, Postman).
•	Componente:
1.	API Layer (Flask/FastAPI): Gestionează request-urile de tip POST /play sau GET /status.
2.	Playback Controller: O clasă care gestionează procesul sistemului de operare (Subprocess) pentru player-ul video.
3.	Media Store: Un folder local unde sunt stocate fișierele .mp4.
API Design
•	POST /play?scenario_id=banana_waste: Pornește un videoclip specific. Dacă un clip rulează deja, serviciul oprește procesul anterior și pornește noul clip (preempțiune).
•	POST /stop: Oprește orice redare activă.
•	GET /status: Întoarce starea curentă (IDLE, PLAYING, ERROR).
Suport pentru Testare Automatizată
Design-ul permite sincronizarea: testul automat trimite comanda de play, așteaptă răspunsul 200 OK, apoi interoghează sistemul Winnow Vision pentru a vedea dacă a detectat corect obiectul din video.

3. Instrucțiuni de rulare (README.md)
Cum rulezi prototipul:
1.	Instalează Python 3.x.
2.	Instalează dependențele: pip install flask.
3.	Asigură-te că vlc este în PATH-ul sistemului tău.
4.	Creează un folder numit videos și adaugă un fișier de test (ex: apple_waste.mp4).
5.	Rulează scriptul: python main.py.
6.	Testează cu un tool precum curl:
o	curl -X POST http://localhost:5000/play?scenario_id=apple_waste

Limitări și îmbunătățiri viitoare:
•	Limitare: Prototipul presupune că player-ul video se închide corect.
•	Îmbunătățire: -Adăugarea unui log de evenimente pentru a corela exact ora la care a pornit clipul cu log-urile din Winnow Vision.
-Folosirea unei librării native (ex: python-vlc) pentru un control mai fin asupra frame-urilor (pauză, seek la un anumit timestamp).
-O interfață web simplă pentru declanșare manuală în timpul debugging-ului.
