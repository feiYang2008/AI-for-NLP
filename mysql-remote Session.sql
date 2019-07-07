SELECT content FROM news_content LIMIT 100;

SELECT count(content) FROM news_content WHERE content like '新华社%';  

Describe news_content;

SELECT count(content) from news_content;

SELECT * from sqlResult_1558435 limit 100;

select count(*), (select count(*) from sqlResult_1558435) 
from sqlResult_1558435 where source like '%新华%' limit 100;

select * from sqlResult_1558435 into outfile '/home/yikang/Desktop/AI-for-NLP/news.tsv'
FIELDS TERMINATED BY '\t'
ENCLOSED BY '"'
LINES TERMINATED BY '\n';

select content, source from sqlResult_1558435 
where content like '新华%'
limit 100;