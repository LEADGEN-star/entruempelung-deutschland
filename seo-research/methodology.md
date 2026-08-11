# SEO-Research Methodology — entruempelung-deutschland.com
**Erstellt:** 2026-08-11  
**Analyst:** Senior SEO-Strategie-Analyse  
**Ziel:** Datenbasierte Priorisierung deutscher Städte für Local-SEO im Bereich Entrümpelung / Haushaltsauflösung / Lead-Generierung

---

## 1. Datenlage & Transparenz

### Was gemessen wurde (Primärdaten)
| Metrik | Quelle | Typ |
|--------|--------|-----|
| Anbieteranzahl je Stadt | raeumungsfinder.de (Recherche Aug 2026) | GEMESSEN |
| Bundesland / Gemeindezugehörigkeit | Destatis-Gemeindeverzeichnis (gesperrt via Proxy, Fallback: Wikipedia-Daten + Eigenrecherche) | GEMESSEN |
| Einwohnerzahl | Destatis-Stand 31.12.2024, via Wikipedia-Recherche | GEMESSEN |
| Dominant-Anbieter in SERPs | Google-Suche Aug 2026 | GEMESSEN |

### Was geschätzt wurde (Proxy-Daten)
| Metrik | Proxy | Begründung |
|--------|-------|------------|
| Hauptkeyword-Suchvolumen | Bevölkerung × Branchenkoeffizient | Kein direkter API-Zugriff auf Google KP, Ahrefs, Semrush verfügbar. Koeffizient: ~0,45 Suchen/1.000 EW/Monat für Hauptkeyword basierend auf öffentlich veröffentlichten Snippets und Branchenbenchmarks |
| Cluster-Volumen | Hauptvolumen × 3,2 (Multiplikator) | Ergibt sich aus typischen Keyword-Clustern: entrümpelung + haushaltsauflösung + wohnungsauflösung + kosten + firma + günstig + keller + dachboden ≈ 3,2× Hauptvolumen gemäß Branchenanalyse |
| CPC | Branchenwert Home Services DE | Allg. Marktwert für Gebäudedienstleistungen: ca. 2,50–6,00 € je nach Stadt. Kein stadtscharfer Wert verfügbar. |
| Keyword-Difficulty (KD) | Anbieteranzahl × Proxy | Inverse Relation: mehr Anbieter = höhere KD |

**WICHTIG:** Alle Suchvolumina in cities.csv sind als SCHÄTZUNGEN markiert (Spalte `source`). Sie ersetzen KEINE eigene Keyword-Planner- oder Ahrefs-Abfrage. Vor Umsetzung müssen Volumina verifiziert werden.

---

## 2. Scoring-Modell

**Gesamtscore 0–100** aus 6 gewichteten Teilscores:

```
Total = Demand(35) + CommercialIntent(20) + MarketSize(15) + Competition(15) + ClusterPotential(10) + RankingChance(5)
```

### 2.1 Suchnachfrage / Demand (max. 35 Punkte)

```
demand_score = 35 × min(log10(Einwohner / 30.000) / log10(3.662.000 / 30.000), 1.0)
```

- Normiert auf Berlin als Maximum (3,66 Mio EW = 35 Punkte)
- Skalierung: logarithmisch (realistischer als linear, weil Keyword-Volumen nicht linear mit EW wächst)
- Basis 30.000 EW = Untergrenze für Städte mit messbarem Keyword-Volumen

### 2.2 Kommerzielle Suchintention (max. 20 Punkte)

Skala 0–4 (analog Bewertungsschema):
- 0 = rein informativ  
- 1 = Recherche  
- 2 = kommerzielle Untersuchung  
- 3 = hohe Kaufintention  
- 4 = unmittelbare Auftragsintention  

**„Entrümpelung [Stadt]"** → Intent = 4 (unmittelbare Auftragsintention)  
→ commercial_intent_score = 4/4 × 20 = **17 Punkte** (leichter Abzug wegen Informations-Beimischung in einigen Märkten)

Cluster-Durchschnitt (kosten, firma, günstig, etc.): Intent ~3,5 → wird für Gesamtbewertung berücksichtigt.

### 2.3 Einwohner / Marktgröße (max. 15 Punkte)

```
market_score = 15 × min(log10(Einwohner / 30.000) / log10(3.662.000 / 30.000), 1.0)
```

(Gleiche Normierung wie demand_score, andere Gewichtung)

### 2.4 SEO-Wettbewerb (max. 15 Punkte) — INVERTIERT

**Niedrigerer Wettbewerb = höherer Score**

```
competition_score = 15 × max(0, 1 - log10(max(1, anbieter_count)) / log10(1.043))
```

- Basis: raeumungsfinder.de-Anbieteranzahl je Stadt (gemessen Aug 2026)
- Berlin mit 1.043 Anbietern = Maximum = 0 Punkte
- Logarithmische Inverse: 10 Anbieter → ~10 Punkte, 5 Anbieter → ~11 Punkte

**Bekannte Messwerte (raeumungsfinder.de, Aug 2026):**
- Berlin: 1.043, München: 229, Hamburg: 153, Bremen: 133, Hannover: 124
- Köln: 96, Frankfurt: 89, Stuttgart: 77, Dortmund: 77, Düsseldorf: 74
- Nürnberg: 68, Essen: 60, Fürstenfeldbruck: 8

**Schätzwerte** (wo nicht direkt gemessen) basieren auf proportionaler Extrapolation aus Bevölkerungsdichte-Koeffizient (~0,11 Anbieter/1.000 EW für Großstädte, höher für Metropolen).

### 2.5 Umland-/Clusterpotenzial (max. 10 Punkte)

Bewertet, ob eine Stadt Teil eines dichten Ballungsraums mit vielen potenziellen Folgeseiten ist:

| Bewertung | Punkte | Beispiel |
|-----------|--------|---------|
| Nationaler Metropolkern | 9–10 | Berlin, München |
| Großstadtkern im Verbund | 8–9 | Köln (mit Bonn, Leverkusen), Ruhrgebiet |
| Regionaler Mittelzentrum | 5–7 | Hannover, Nürnberg, Stuttgart |
| Eigenständige Mittelstadt | 3–5 | Kassel, Freiburg, Rostock |
| Kleinstadt ohne Verbund | 2–3 | Flensburg, Schwerin |
| Vorort / Cluster-Satellit | 7–9 | Dachau (München), Offenbach (Frankfurt) |

### 2.6 Aktuelle Ranking-Chance (max. 5 Punkte)

Kombination aus inversem Wettbewerb + Schwäche der Incumbents:

```
ranking_chance = min(5, competition_score / 15 × 5 × adjustment)
```

adjustment = 0.8–1.2 basierend auf beobachteter Qualität der Top-10-Rankings (thin content = +20%, starke Domains = –20%)

---

## 3. Hauptwettbewerber (SERP-Analyse, Aug 2026)

Dominante Domains in den Entrümpelung-SERPs:

| Domain | Typ | Bewertung |
|--------|-----|-----------|
| entsorgo.de | Nationales Buchungsportal | Stark, viele Stadtseiten, transaktional |
| ruempel-fritz.de | Nationaler Marktführer-Claim | Sehr stark, TV-bekannt, viele Bewertungen |
| aflex.de | Nationales Service-Netzwerk | Stark, fixpreis-fokussiert |
| raeumungsfinder.de | Verzeichnis/Aggregator | Sehr hohe Sichtbarkeit, 10.521 Anbieter gelistet |
| trustlocal.de | Bewertungsportal | Starke lokale Präsenz |
| werkenntdenbesten.de | Bewertungsaggregator (52 Portale) | Gut etabliert |
| listando.de | Lokales Verzeichnis | Mittel |
| golocal.de | Bewertungsplattform | Mittel |

**Strategie-Implikation:** entruempelung-deutschland.com konkurriert direkt mit Aggregatoren und Buchungsportalen. Differenzierung durch lokale Expertise, Stadt-spezifischen Content und starke interne Verlinkung ist entscheidend.

---

## 4. Keyword-Intent-Klassifikation

| Keyword-Typ | Beispiel | Intent-Wert |
|-------------|---------|-------------|
| unmittelbare Auftragsintention | „Entrümpelung München" | 4 |
| unmittelbare Auftragsintention | „Haushaltsauflösung sofort Berlin" | 4 |
| hohe Kaufintention | „Entrümpelung Kosten Frankfurt" | 3 |
| hohe Kaufintention | „Entrümpelung Firma Hamburg" | 3 |
| hohe Kaufintention | „Entrümpelung Preis Stuttgart" | 3 |
| kommerzielle Untersuchung | „Entrümpelung Erfahrungen" | 2 |
| Recherche | „Wie viel kostet eine Entrümpelung" | 1 |
| rein informativ | „Selbst entrümpeln Tipps" | 0 |

**Lead-Gen-Fokus:** Priorität auf Intent 3–4. Informationelle Keywords (0–1) haben geringen direkten Lead-Wert, können aber für interne Verlinkung und Topical Authority genutzt werden.

---

## 5. Keyword-Cluster je Stadt

Jede Stadtseite sollte folgende Keywords primär abdecken:

**Primär (Intent 4):**
- entrümpelung [stadt]
- haushaltsauflösung [stadt]
- wohnungsauflösung [stadt]
- entrümpelung [stadt] günstig
- entrümpelungsfirma [stadt]

**Sekundär (Intent 3):**
- entrümpelung [stadt] kosten
- entrümpelung [stadt] preise
- entrümpelung [stadt] festpreis
- kellerentrümpelung [stadt]
- dachbodenräumung [stadt]

**Tertiär (Intent 2–3):**
- sperrmüll abholung [stadt]
- möbelentsorgung [stadt]
- nachlassräumung [stadt]
- messie-wohnung räumung [stadt]

---

## 6. Doorway-Page-Warnung

**WARNUNG:** Seiten, die ausschließlich aus automatisch ausgetauschten Städtenamen bestehen, verstoßen gegen die Google-Qualitätsrichtlinien (Doorway Pages, Panda-relevanter Thin Content).

**Mindestanforderungen je Stadtseite:**
1. Einzigartiger Einleitungstext mit lokalen Bezügen (Stadtteile, Besonderheiten, Entsorgungsbetriebe)
2. Lokale FAQ (z.B. „Was kostet eine Kellerentrümpelung in [Stadt]?")
3. Spezifische Preisbeispiele oder Preisbereiche für die Region
4. Lokale Trust-Signale (Google Business, ggf. regionale Auszeichnungen)
5. Stadtteile als interne Verlinkung
6. Schemamarkup: LocalBusiness + FAQPage + HowTo (wo sinnvoll)

---

## 7. Quellen

| Quelle | URL | Datum | Typ |
|--------|-----|-------|-----|
| raeumungsfinder.de Stadtseiten | raeumungsfinder.de | Aug 2026 | GEMESSEN |
| Google SERP-Analyse „Entrümpelung Berlin/München etc." | google.de | Aug 2026 | GEMESSEN |
| Destatis Gemeindeverzeichnis (Einwohnerzahlen 31.12.2024) | destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/ | Aug 2026 (via Websuche) | GEMESSEN (Proxy) |
| Wikipedia Liste Groß- und Mittelstädte | de.wikipedia.org/wiki/Liste_der_Groß-_und_Mittelstädte_in_Deutschland | Aug 2026 | GEMESSEN (Proxy) |
| Fischer's Online Marketing SEO Entrümpelung | fischers-onlinemarketing.org | Aug 2026 (geblockt) | N/A |
| Google CPC Benchmarks Germany 2025 | codedesign.org, gemprogrammers.com | Aug 2026 | SCHÄTZUNG |
| Allgemein: Branchenkoeffizient Keyword-Volumen | Eigene Berechnung basierend auf Branchenbenchmarks | Aug 2026 | BERECHNUNG |

---

## 8. Methodik-Einschränkungen

1. **Kein direkter Zugriff auf Keyword-Tools:** Google Keyword Planner, Ahrefs, Semrush, Sistrix waren im Rahmen dieser Recherche nicht direkt abfragbar. Alle Suchvolumina sind SCHÄTZUNGEN.
2. **raeumungsfinder.de als Wettbewerbs-Proxy:** Die Anbieteranzahl auf diesem Portal entspricht nicht zwingend der Anzahl aktiver SEO-Wettbewerber, aber ist ein nützlicher Proxy für Marktdichte.
3. **Einwohnerzahlen:** Destatis-Daten (Stand 31.12.2024) konnten nicht direkt abgefragt werden (Domain geblockt). Werte basieren auf aktuellen Wikipedia-Einträgen, die auf Destatis verweisen.
4. **Domain-Authority:** Keine direkten DR/DA-Werte verfügbar (Ahrefs geblockt). Qualitative Einschätzung basierend auf SERP-Beobachtung.

**Empfehlung:** Vor Priorisierung sollten die Schätzwerte durch direkte Keyword-Planner-Abfragen oder ein Semrush/Ahrefs-Abonnement validiert werden.
