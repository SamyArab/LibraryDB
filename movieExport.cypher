LOAD CSV WITH HEADERS FROM "file:///Movies.csv" as line
WITH line
WHERE line.movie_id IS NOT NULL
MERGE (m: Movies {movie_id: line.movie_id})
MERGE (c: Countries {countries: line.country})
MERGE (l: Languages {languages: line.languages})
SET m.title = line. title,
	m.plot = line.plot,
	m.runtime = toFloat(line.runtime)
MERGE (m)-[:SPOKEN_IN]->(l)
MERGE (m)-[:PRODUCED_IN]->(c);