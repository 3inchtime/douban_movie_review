# douban_movie_review

# 豆瓣Top250电影影评排行榜爬虫

结果保存为./data/review.csv，第一列为0或1（好评，差评），第二列为评论内容。

在默认频率下运行大约1小时会反爬虫，大约会抓到18000条，可以更换代理解决。

运行时首先获取Top250的ID列表，保存在./data/top.txt下。

```bash
// 获取豆瓣Top250电影ID
scrapy crawl top
// 抓取豆瓣Top250电影影评
scrapy crawl douban
```