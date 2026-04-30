# 理想汽车 UI 风格规范

## 色盘

| Token | 色值 | 用途 |
|---|---|---|
| `li-green-base` | `#0A1613` | 页面背景 |
| `li-green-card` | `#11241F` | 卡片背景 |
| `li-green-hover` | `#17312A` | 悬浮交互 |
| `li-gold` | `#CBA774` | 主强调色（香槟金） |
| `li-gold-light` | `#E2CDAA` | 浅金色高亮 |

## Tailwind 配置

```javascript
// frontend/tailwind.config.js
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        'li-green-base': '#0A1613',
        'li-green-card': '#11241F',
        'li-green-hover': '#17312A',
        'li-gold': '#CBA774',
        'li-gold-light': '#E2CDAA',
      },
      fontFamily: {
        sans: ['-apple-system', 'BlinkMacSystemFont', '"PingFang SC"', '"Helvetica Neue"', 'sans-serif'],
      },
      borderRadius: { 'li-card': '32px' },
    },
  },
  plugins: [],
}
```

## 全局样式（index.css）

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-li-green-base text-white antialiased;
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", sans-serif;
  }
  ::-webkit-scrollbar { display: none; }
  h1, h2, h3, h4, h5, h6 { @apply text-white font-bold tracking-tight; }
  ::selection { @apply bg-li-gold text-li-green-base; }
}

@layer components {
  .btn-primary {
    @apply bg-li-gold hover:bg-li-gold-light text-li-green-base font-semibold px-6 py-3 rounded-full transition-all duration-300;
  }
  .btn-secondary {
    @apply bg-li-green-card hover:bg-li-green-hover text-white font-medium px-6 py-3 rounded-full transition-colors duration-300 border border-white/10;
  }
  .card {
    @apply bg-li-green-card rounded-li-card p-10 relative overflow-hidden border border-white/5
           hover:bg-li-green-hover transition-all duration-500;
  }
  .card::after {
    content: '';
    @apply absolute -bottom-24 -right-24 w-64 h-64 bg-li-gold/10 rounded-full blur-3xl
           transition-all duration-700 pointer-events-none;
  }
  .input {
    @apply w-full px-4 py-3 bg-li-green-card border border-white/10 rounded-xl text-white
           placeholder:text-white/30 focus:outline-none focus:ring-2 focus:ring-li-gold focus:border-transparent
           transition-all duration-200;
  }
  .text-gradient-gold {
    @apply text-transparent bg-clip-text bg-gradient-to-r from-li-gold via-li-gold-light to-li-gold;
  }
}

@keyframes pulse-slow {
  0%, 100% { opacity: 0.15; }
  50% { opacity: 0.4; }
}
.animate-pulse-slow {
  animation: pulse-slow 4s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
```

## 组件设计模式

### 页面容器

```jsx
<div className="min-h-screen bg-li-green-base p-8">
  <div className="max-w-7xl mx-auto">{/* 内容 */}</div>
</div>
```

### 背景光晕（首屏/重要页面）

```jsx
<div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2
                w-[600px] h-[600px] bg-li-gold/20 rounded-full blur-[120px]
                pointer-events-none animate-pulse-slow" />
```

### 超大标题

```jsx
<h1 className="text-6xl md:text-8xl font-bold tracking-tighter">
  普通文字<span className="text-gradient-gold">金色渐变</span>
</h1>
```

### 卡片（带悬停光晕）

```jsx
<div className="card group cursor-pointer">
  <div className="relative z-10">{/* 内容 */}</div>
</div>
```

### 颜色使用规范

- 页面背景：`bg-li-green-base`
- 卡片背景：`bg-li-green-card`
- 悬浮：`hover:bg-li-green-hover`
- 强调色：`bg-li-gold` / `text-li-gold`
- 渐变文字：`text-gradient-gold`
- 主要文字：`text-white`
- 次要文字：`text-white/50`
- 边框：`border-white/5` 或 `border-white/10`
- 按钮/输入框：`rounded-full` / `rounded-xl`
- 卡片圆角：`rounded-li-card`（32px）
- 过渡：`transition-all duration-300`
