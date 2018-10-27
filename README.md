Description
===========

Implementation of a full text search index based on n-grams.
It takes an arbitrary number of documents into the index. The
search index is stored fully in main memory. A search request
is responded with a list of documents sorted by relevance and
with associated relevance scores.

Requires Python3.5

Changelog
=========

2018-04-29

Document ids now stored as b'' internally.

2018-02-17

Suche in mehreren Dokumenten.
Global eindeutige Dokumenten-Id

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
* Laufzeiten vergleichen mit großen Collections

Server
* Such-Engine standalone mit Funktion des Suchens per API
* Einfügen von Dokumenten per API
* Persistieren des Suchindex
* Große Kollektion mit ext. RAM-Datenbank

Frontend (Google-like)
* Eingabe von Suchbegriffen und Rückgabe von Scores
* Ausgabe von Dokumenten. Markieren der relevanten Suchberiffe in gelb.

Speicherverbrauch und dessen Limits testen.
Profiling. Überwachung des Speicherverbrauchs.

