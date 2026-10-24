# SQL 方言中的中文表与字段注释

只阅读并采用目标数据库对应部分。示例中的对象和说明是演示，修改现有对象前必须核对真实定义、schema 和业务语义。

## PostgreSQL

`COMMENT ON` 写入数据库对象的注释元数据。以下假设 `public.content_document` 及其字段已存在：

```sql
COMMENT ON TABLE public.content_document IS '文档元数据，每行表示一个文档对象';
COMMENT ON COLUMN public.content_document.id IS '文档对象的稳定标识，改名或发布新版本时保持不变';
COMMENT ON COLUMN public.content_document.title IS '文档显示名称，可修改且不作为稳定对象标识';
```

通过数据库目录核对结果，不只检查 SQL 文件中是否存在中文：

```sql
-- 核对表注释；这里的字符串应替换为已确认的实际 schema 和表名。
SELECT obj_description('public.content_document'::regclass, 'pg_class') AS table_comment;

-- 核对当前表的业务列，排除系统列和已删除列。
SELECT
    a.attname AS column_name,
    col_description(a.attrelid, a.attnum) AS column_comment
FROM pg_catalog.pg_attribute AS a
WHERE a.attrelid = 'public.content_document'::regclass
  AND a.attnum > 0
  AND NOT a.attisdropped
ORDER BY a.attnum;
```

重新设置会替换旧注释；`IS NULL` 移除注释。需要回退时记录并恢复原值，不一律清空。操作需要相应权限且会获取锁，按项目迁移窗口执行。注释可被其他数据库用户看到，不保存敏感内容。

## MySQL

新建表可以在列定义和表选项中声明 `COMMENT`。下面只演示注释语法，主键类型不指定对象身份方案；未展开审计字段和其他业务列，不能直接作为完整业务表模板：

```sql
CREATE TABLE content_document (
    id BIGINT NOT NULL COMMENT '文档对象的稳定标识，由调用方按既有身份规则提供',
    title VARCHAR(200) NOT NULL COMMENT '文档显示名称，可修改且不作为稳定对象标识',
    PRIMARY KEY (id)
) COMMENT = '文档元数据，每行表示一个文档对象';
```

修改表注释可使用 `ALTER TABLE content_document COMMENT = '新的中文说明'`。修改列注释前，先通过 `SHOW CREATE TABLE content_document` 等方式读取真实定义；使用 `MODIFY COLUMN` 或 `CHANGE` 时，须保留适用的类型、可空性、默认值、自增、字符集、排序规则、生成列和其他属性。不要复制一个简化定义覆盖现有列。

验证实际元数据：

```sql
SELECT TABLE_COMMENT
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'content_document';

SELECT COLUMN_NAME, COLUMN_COMMENT
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'content_document'
ORDER BY ORDINAL_POSITION;
```

当前连接数据库不是目标库时，显式指定已确认的数据库名称。核对升级前后的完整定义，注释修改不能无意改变其他列属性。

## SQLite 及其他数据库

SQLite 的 `--` 和 `/* ... */` 是 SQL 文本注释，没有与上述 PostgreSQL、MySQL 相同的原生表列注释接口。不要生成 `COMMENT ON` 或 MySQL 列 `COMMENT` 语法。

采用项目已经维护的模型说明、相邻 SQL 注释或数据字典，并明确这不等于数据库原生表列元数据注释。不要仅为兼容注释新建业务表或重建已有表。其他引擎查阅其官方文档，不能机械套用以上方言。

## 官方依据

- [PostgreSQL COMMENT](https://www.postgresql.org/docs/current/sql-comment.html)
- [PostgreSQL 注释查询函数](https://www.postgresql.org/docs/current/functions-info.html#FUNCTIONS-INFO-COMMENT-TABLE)
- [MySQL CREATE TABLE](https://dev.mysql.com/doc/refman/8.4/en/create-table.html)
- [MySQL ALTER TABLE](https://dev.mysql.com/doc/refman/8.4/en/alter-table.html)
- [SQLite SQL 注释语法](https://www.sqlite.org/lang_comment.html)

示例按这些文档核对；实施时仍以项目实际数据库版本和迁移工具能力为准。
