### ch2sql
目标是用自然语言查询电子表格中的数据(区别于关系型数据库,我们只关心单表问题) . 总体思路是以查询输入语句和电子表格信息为输入, 结合自然语言处理工具将查询语句映射到数据库语义相关的节点中,最后转换为SQL类似的JSON表示结构
### 特性列表
- 结合数据表语义分词, 确保字段名,常见的值不会被分词算法拆分.例如: 'APP下载量' 是表格的一个属性名, 不能拆分为'APP'和'下载量'两个词
- 用词向量技术映射属性节点和值节点
