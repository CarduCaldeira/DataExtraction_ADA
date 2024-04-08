SELECT
    title,
    url,
    author,
    description,
    image_url,
    content,
    source,
    tags,
    publication_date,
    CASE WHEN query0 THEN 1 ELSE 0 END AS query0,
    CASE WHEN query1 THEN 1 ELSE 0 END AS query1,
    CASE WHEN query2 THEN 1 ELSE 0 END AS query2
FROM (
    SELECT
        title,
        url,
        author,
        description,
        image_url,
        content,
        source,
        tags,
        publication_date,
        query0,
        query1,
        query2,
        RANK() OVER (PARTITION BY title, url ORDER BY publication_date DESC) AS rank_value
    FROM
        raw_db.news
) AS ranked_news
WHERE
    rank_value = 1;