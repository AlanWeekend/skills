# 中文 JSDoc 示例

以下示例展示普通类型、函数与回调的中文接口契约。

## 类型和函数

```typescript
/** 一页数据；T 表示这一页中每条业务记录的类型。 */
export interface PageResult<T> {
  /** 当前页记录；空数组表示没有可展示的数据。 */
  items: T[];
  /** 下一页游标；null 表示已经到达末页。 */
  nextCursor: string | null;
}

/**
 * 判断分页结果是否允许继续加载。
 * @param page - 服务器返回的当前页结果。
 * @returns 存在下一页游标时为 true；空字符串不被视为有效游标。
 */
export function hasNextPage<T>(page: PageResult<T>): boolean {
  return page.nextCursor !== null && page.nextCursor.length > 0;
}

/**
 * 去除标题首尾空白，并校验标题包含实际内容。
 * @param title - 用户输入的原始标题，不修改调用方持有的值。
 * @returns 可以用于提交或展示的非空标题。
 * @throws {Error} 标题去除空白后为空时抛出。
 */
export function requireTitle(title: string): string {
  const normalized = title.trim();
  if (normalized.length === 0) {
    throw new Error('标题不能为空');
  }
  return normalized;
}
```

## 匿名回调

```typescript
/** 提取非空白消息，保留原始顺序和文本，供列表展示。 */
export function visibleMessages(messages: readonly string[]): string[] {
  return messages.filter((message) => message.trim().length > 0);
}
```

## 边界

- JS 需要时可在 JSDoc 中声明类型；TS 的中文描述优先补充类型无法表达的业务含义。
- Promise 返回值说明何时完成、是否可能取消；不要仅写“返回一个 Promise”。
- 框架的回调按照合法语法放置接口说明，不为满足注释数量改写 JSX 或业务逻辑。
