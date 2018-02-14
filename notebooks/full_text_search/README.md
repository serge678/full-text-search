
Changelog
=========

2018-02-14

Eliminierung der Leerzeichen, Punktuation. Trigramme spannen nicht zwei Worte auf.
Eliminierung der Stopp-Wörter.

2018-02-13

Erste Implementierung einer Volltextsuche mit Trigrams.
Nur ein Dokument im Index. Search-Index und naiver Search-Score, der nur Anzahl getroffener
Trigrams zählt.

Search-Index berücksichtigt alle Vorkommen eines Trigrams im Dokument.
Search-Score berücksichtigt die Nähe der Trigram im Suchbegriff.
Die Abstandmetrik ist die relative Distanz der Trigramme im Suchbergiff und im Index.