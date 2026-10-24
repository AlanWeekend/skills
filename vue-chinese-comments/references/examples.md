# Vue 页面与组件示例

以下组件只负责展示和收集输入，不直接调用 API。父组件负责处理 send 事件和 loading 状态。

```vue
<!--
用途：会话消息面板，展示消息列表并收集用户输入。
职责：发送非空白消息、显示提交状态；实际请求由父组件处理。
输入与事件：接收 messages 和 loading，通过 send 事件上报待发送文本。
-->
<script setup lang="ts">
import { computed, ref } from 'vue';

/** 消息的展示数据，不包含服务端权限或持久化行为。 */
interface MessageView {
  /** 稳定的消息编号，用于列表节点复用。 */
  id: string;
  /** 以普通文本展示的消息内容。 */
  content: string;
}

/** 父组件传入的消息及提交状态，组件内部不修改这些输入。 */
const props = withDefaults(defineProps<{
  /** 当前会话的消息，按父组件提供的顺序展示。 */
  messages: readonly MessageView[];
  /** 父组件处理发送请求期间为 true，防止重复提交。 */
  loading?: boolean;
}>(), { loading: false });

/** send 在输入有效且未提交时触发，载荷是已去除首尾空白的文本。 */
const emit = defineEmits<{
  send: [message: string];
}>();

/** 尚未发送的输入，由本组件维护，与父组件的消息列表分开保存。 */
const draft = ref('');

/** 根据输入内容和父级提交状态计算是否可发送，不发起请求。 */
const canSend = computed(() => draft.value.trim().length > 0 && !props.loading);

/** 校验当前输入，向父组件发送消息后清空草稿；请求失败反馈由父组件负责。 */
function sendMessage(): void {
  // 与按钮禁用状态保持同一规则，也防止其他入口调用时绕过校验。
  if (!canSend.value) {
    return;
  }

  // 只上报规范化文本，不在此组件中直接新增消息或调用接口。
  emit('send', draft.value.trim());
  // 清空仅代表输入已上报，不表示服务端已经保存或 Agent 已执行成功。
  draft.value = '';
}
</script>

<template>
  <section aria-label="会话消息">
    <!-- 展示父组件提供的消息；无消息时展示空状态，不在条件链中间插注释。 -->
    <ul v-if="props.messages.length > 0">
      <li v-for="message in props.messages" :key="message.id">{{ message.content }}</li>
    </ul>
    <p v-else>暂无消息</p>

    <!-- 输入和发送区域：阻止浏览器默认提交，由组件向父级上报文本。 -->
    <form @submit.prevent="sendMessage">
      <label>消息内容<input v-model="draft" :disabled="props.loading" /></label>
      <button type="submit" :disabled="!canSend">发送</button>
    </form>

    <!-- 父级提交过程的反馈，不能据此推断 Agent 的最终执行结果。 -->
    <p v-if="props.loading" role="status">正在提交</p>
  </section>
</template>
```

补注释时应据实记录已有约定，不顺带改变组件接口。

## 订阅与监听的说明

对 watch 注释要区分首次执行、后续变化及 DOM 更新时机；对轮询、监听器或订阅写清注册位置、停止条件和实际清理位置。代码没有清理时，应报告缺口，不能只添加“卸载时自动清理”的注释。
