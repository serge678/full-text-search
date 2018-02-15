Changelog
=========

2018-02-14

Eliminierung der Leerzeichen, Punktuation, Großbuchstaben.
Trigramme spannen nicht zwei Worte auf.
Eliminierung der Stopp-Wörter.

2018-02-13

Erste Implementierung einer Volltextsuche mit Trigrams.
Nur ein Dokument im Index. Search-Index und naiver Search-Score, der nur Anzahl getroffener
Trigrams zählt.

Search-Index berücksichtigt alle Vorkommen eines Trigrams im Dokument.
Search-Score berücksichtigt die Nähe der Trigram im Suchbegriff.
Die Abstandsmetrik ist die relative Distanz der Trigramme im Suchbergiff und im Index.

Wishlist
========

Auf mehrere Dokumente erweitern.
* Naiv: Liste von SEARCH_INDEXes führen
* Intelligent: SEARCH_INDEX über alle Dokumente gleichzeitig
* Laufzeiten vergleichen mit großen Collections

Speicherverbrauch und dessen Limits testen.
Profiling. Überwachung des Speicherverbrauchs.

Speichern und Laden des Suchindexes.

Suchindex mit Redis.

