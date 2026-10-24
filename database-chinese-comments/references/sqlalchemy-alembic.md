# SQLAlchemy 与 Alembic 的中文数据库注释

只在项目实际使用这些工具时采用本参考。先检查锁定版本、模型组织、迁移头和 schema 配置，不为添加注释改造项目架构。

## SQLAlchemy 模型

以下 SQLAlchemy 2.x 示例只说明注释的放置位置，UUID 类型、表名和长度不是通用规范，也没有规定 ID 生成方式。仅节选注释相关字段，完整业务模型还应按项目约定补齐审计字段及其他业务列：

```python
"""演示文档模型的表注释和字段注释，不负责业务 ID 分配。"""

from uuid import UUID

from sqlalchemy import String, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """为示例模型提供声明式映射基类。"""


class Document(Base):
    """保存一个文档对象的当前元数据，版本记录由独立模型维护。"""

    __tablename__ = "content_document"
    __table_args__ = {"comment": "文档元数据，每行表示一个文档对象"}

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        comment="文档对象的稳定标识，改名或发布新版本时保持不变",
    )
    title: Mapped[str] = mapped_column(
        String(200),
        comment="文档显示名称，可修改且不作为稳定对象标识",
    )
```

- Core 风格用 `Table(..., comment=...)` 和 `Column(..., comment=...)`；声明式列用 `mapped_column(..., comment=...)`。
- 已有 `__table_args__` 的约束、索引和选项必须保留，只合并注释；不能用示例字典整体覆盖。
- `Column.doc`、Python Docstring、Pydantic 字段描述不等于数据库列注释。
- 模型修改只改变目标元数据，不表示存量数据库已更新；通过项目迁移机制生效，不用 `create_all()` 代替升级。

## Alembic 迁移

新建表通过 `op.create_table(..., comment=...)`，列通过 `sa.Column(..., comment=...)` 声明注释。存量表用 `op.create_table_comment`，存量列用 `op.alter_column(..., comment=...)`。

以下是已有 Alembic revision 的函数片段，不是完整迁移文件；保留项目生成的 revision 元信息。示例假设该 PostgreSQL 项目的旧表注释为“文档信息”、旧字段注释为“文档名称”，实际必须用已核实的旧值：

```python
from alembic import op


def upgrade() -> None:
    """明确文档表的记录粒度和标题字段的业务含义。"""
    op.create_table_comment(
        "content_document",
        "文档元数据，每行表示一个文档对象",
        existing_comment="文档信息",
    )
    op.alter_column(
        "content_document",
        "title",
        comment="文档显示名称，可修改且不作为稳定对象标识",
        existing_comment="文档名称",
    )


def downgrade() -> None:
    """恢复此次迁移前的注释，保留字段定义和现有数据。"""
    op.alter_column(
        "content_document",
        "title",
        comment="文档名称",
        existing_comment="文档显示名称，可修改且不作为稳定对象标识",
    )
    op.create_table_comment(
        "content_document",
        "文档信息",
        existing_comment="文档元数据，每行表示一个文档对象",
    )
```

- 项目使用非默认 schema 时，在各操作中明确相同的 `schema`。旧值为无注释时，恢复为无注释，而非随意造一个说明。
- `existing_comment` 描述已有值，不会自动代写 `downgrade()`；按实际旧状态编写恢复操作。
- MySQL 改列需完整列规格，核对 `existing_type`、`existing_server_default`、`existing_nullable`、自增及其他实际属性，必要时补齐方言参数；不能把上述 PostgreSQL 片段原样当作跨库迁移。
- 代码里的默认值不是服务器默认值，不能混用 `default` 与 `server_default`。
- `--autogenerate` 生成的是待审查迁移；核对项目版本和方言是否检测注释差异，不把未生成操作误判成“不需要迁移”。
- 已应用迁移默认追加修订，不回改历史；仅注释变更不夹带无关 schema 差异。SQLite 不支持原生表列注释时，说明限制，不能靠 batch 重建表伪装实现。

## 验证顺序

1. 核对受影响表与列的模型注释，以及本次 revision 的升降级内容。
2. 通过离线 SQL 或项目现有检查审查目标方言生成结果；这一步不证明实际落库。
3. 在授权的兼容测试库验证初始化或存量升级，查询真实目录注释；需要验证回退时核对旧注释及其他列属性。
4. 测试库回退后恢复到预期迁移头；如果没有数据库环境，交付时注明仅通过静态或离线验证。

## 官方依据

- [SQLAlchemy Table 与 Column 元数据参数](https://docs.sqlalchemy.org/en/20/core/metadata.html)
- [SQLAlchemy mapped_column](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column)
- [Alembic 操作 API](https://alembic.sqlalchemy.org/en/latest/ops.html)
- [Alembic 自动生成迁移及限制](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)
