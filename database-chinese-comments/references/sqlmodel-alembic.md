# SQLModel 与 Alembic 的中文数据库注释

项目采用 SQLModel 时读取本参考。SQLAlchemy 仍是底层数据库能力；沿用项目锁定版本和已有模型、迁移组织，不为添加注释切换 ORM 或另建一套 DeclarativeBase 业务模型。

## 模型注释

以下是放入已有 `SQLModel` 的 `table=True` 类的局部片段，不是完整业务表；保留原表名、业务字段、审计字段、约束和模型组织：

```python
# 已有文件应导入 sqlmodel 的 Field；不要在类体中导入。
__table_args__ = {"comment": "文档元数据，每行表示一个文档对象"}

title: str = Field(
    max_length=200,
    description="文档显示名称，可修改且不作为稳定对象标识",
    sa_column_kwargs={
        "comment": "文档显示名称，可修改且不作为稳定对象标识",
    },
)
```

- `__table_args__` 中的 `comment` 是表注释；已有索引、约束、schema 等选项必须保留并合并，不能直接用示例字典覆盖。
- `Field(description=...)` 用于模型或接口描述，不会代替 SQLAlchemy 列的数据库 `comment`；需要两种载体时，分别声明并保持中文语义一致。
- 没有自定义 `sa_column` 时，可通过 `sa_column_kwargs={"comment": ...}` 将注释传给底层列。已有 `sa_column=Column(...)` 时，在该 `Column` 上维护 `comment` 并保留原属性，不再同时传 `sa_column_kwargs`。
- 不把修改注释变成主键、列类型、默认值或可空性的修改。字段类型及长度按真实业务确定，不能照抄示例的长度。
- SQLModel 表模型与创建、更新、响应模型按接口职责分开。不要仅为复用描述把内部字段公开，也不把表实例构造等同于已验证外部输入。

## Alembic 元数据与迁移

在项目已有的 Alembic `env.py` 中，先按实际导入路径完成所有业务表模型注册，再使用目标元数据：

```python
from sqlmodel import SQLModel

# 执行到这里前，已有业务模型注册入口必须完成导入。
target_metadata = SQLModel.metadata
```

仅导入 `SQLModel` 本身不会自动导入项目的业务表。审查生成差异，防止元数据遗漏被误认为删表；通过迁移管理版本，不把 `SQLModel.metadata.create_all()` 当成存量升级机制。

表和列注释仍通过 Alembic 的注释操作落库；目标数据库的支持情况、已应用迁移的维护及恢复旧注释规则与 SQLAlchemy 场景一致。编写具体迁移时按需阅读 [sqlalchemy-alembic.md](sqlalchemy-alembic.md) 的迁移部分，不必将 SQLModel 模型改写为其示例映射。

## 验证

- 检查 SQLModel 表元数据中的表注释、各字段 `comment`，以及需要公开的字段描述；不能只检查 `description`。
- 使用目标方言核对生成的 DDL 和迁移；离线编译不等于数据库已更新。
- 在授权的兼容测试库升级并查询实际目录注释；未连接数据库时，明确只完成结构、模型元数据或离线 SQL 检查。

## 官方依据

- [SQLModel Field 与列配置实现](https://github.com/fastapi/sqlmodel/blob/main/sqlmodel/main.py)
- [SQLModel 多模型与接口边界](https://sqlmodel.tiangolo.com/tutorial/fastapi/multiple-models/)
- [SQLModel 元数据注册顺序](https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#sqlmodel-metadata-order-matters)
- [Alembic 自动迁移与目标元数据](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)

以项目实际锁定版本验证接口；教程里的 SQLite 或内存示例不代表生产环境的持久化和注释能力。
