<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-4xl font-bold text-center text-gray-900 mb-8">
        📰 临桂资讯平台
      </h1>
      <p class="text-center text-gray-600 mb-12">
        桂林市临桂区官方新闻资讯平台
      </p>

      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
        <div class="bg-white rounded-lg shadow-lg p-6">
          <div class="text-4xl mb-4">👥</div>
          <h3 class="text-xl font-semibold mb-2">庞大用户系统</h3>
          <ul class="text-sm text-gray-600 space-y-1">
            <li>✅ 邮箱注册登录</li>
            <li>✅ 6位验证码邮件</li>
            <li>✅ 个人中心设置</li>
            <li>✅ 个人信息码</li>
            <li>✅ 好友添加</li>
            <li>✅ 私信聊天</li>
          </ul>
        </div>

        <div class="bg-white rounded-lg shadow-lg p-6">
          <div class="text-4xl mb-4">💰</div>
          <h3 class="text-xl font-semibold mb-2">双重支付系统</h3>
          <ul class="text-sm text-gray-600 space-y-1">
            <li>✅ Stripe支付</li>
            <li>✅ 支付宝支付</li>
            <li>✅ 微信支付</li>
            <li>✅ 月度订阅 19.9元</li>
            <li>✅ 年度订阅 199元</li>
            <li>✅ 永久会员 599元</li>
          </ul>
        </div>

        <div class="bg-white rounded-lg shadow-lg p-6">
          <div class="text-4xl mb-4">📰</div>
          <h3 class="text-xl font-semibold mb-2">新闻爬虫系统</h3>
          <ul class="text-sm text-gray-600 space-y-1">
            <li>✅ 新华网爬取</li>
            <li>✅ 桂林市政府爬取</li>
            <li>✅ 临桂区政府爬取</li>
            <li>✅ 永久保存</li>
            <li>✅ 历史查看</li>
            <li>✅ 实时更新</li>
          </ul>
        </div>

        <div class="bg-white rounded-lg shadow-lg p-6">
          <div class="text-4xl mb-4">🌐</div>
          <h3 class="text-xl font-semibold mb-2">语言转译</h3>
          <ul class="text-sm text-gray-600 space-y-1">
            <li>✅ 中文简体/繁体</li>
            <li>✅ 英语/日语/韩语</li>
            <li>✅ 粤语/广西壮话</li>
            <li>✅ 法语/德语等</li>
            <li>✅ TTS语音播报</li>
            <li>✅ 多种音色</li>
          </ul>
        </div>

        <div class="bg-white rounded-lg shadow-lg p-6">
          <div class="text-4xl mb-4">🎬</div>
          <h3 class="text-xl font-semibold mb-2">画质切换</h3>
          <ul class="text-sm text-gray-600 space-y-1">
            <li>✅ 流畅480P</li>
            <li>✅ 标清720P</li>
            <li>✅ 高清1080P</li>
            <li>✅ 超清2160P</li>
            <li>✅ 自动适应</li>
            <li>✅ 省流模式</li>
          </ul>
        </div>

        <div class="bg-white rounded-lg shadow-lg p-6">
          <div class="text-4xl mb-4">📥</div>
          <h3 class="text-xl font-semibold mb-2">文件下载</h3>
          <ul class="text-sm text-gray-600 space-y-1">
            <li>✅ PDF文档</li>
            <li>✅ Word文档</li>
            <li>✅ Excel表格</li>
            <li>✅ PPT演示</li>
            <li>✅ MP4视频</li>
            <li>✅ MP3音频</li>
          </ul>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-lg p-8 mb-8">
        <h2 class="text-2xl font-bold mb-4">📰 新闻分类</h2>
        <div class="grid md:grid-cols-4 gap-4">
          <div class="bg-blue-50 p-4 rounded-lg">
            <h3 class="font-semibold text-blue-800">国家时政（免费）</h3>
            <p class="text-sm text-blue-600">新华网、人民网等</p>
          </div>
          <div class="bg-green-50 p-4 rounded-lg">
            <h3 class="font-semibold text-green-800">桂林临桂（免费）</h3>
            <p class="text-sm text-green-600">桂林市政府、临桂区政府</p>
          </div>
          <div class="bg-purple-50 p-4 rounded-lg">
            <h3 class="font-semibold text-purple-800">社会热点（订阅）</h3>
            <p class="text-sm text-purple-600">腾讯新闻等</p>
          </div>
          <div class="bg-orange-50 p-4 rounded-lg">
            <h3 class="font-semibold text-orange-800">财经商业（订阅）</h3>
            <p class="text-sm text-orange-600">东方财富网等</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-lg p-8 mb-8">
        <h2 class="text-2xl font-bold mb-4">📋 订阅权益</h2>
        <div class="grid md:grid-cols-3 gap-6">
          <div class="border-2 border-blue-200 rounded-lg p-6 text-center">
            <h3 class="text-xl font-bold text-blue-600 mb-2">月度订阅</h3>
            <p class="text-3xl font-bold mb-4">¥19.9<span class="text-sm font-normal">/月</span></p>
            <ul class="text-sm text-gray-600 space-y-2 text-left">
              <li>✅ 全部新闻内容</li>
              <li>✅ 语音播报</li>
              <li>✅ 语言转译</li>
              <li>✅ 文件下载</li>
              <li>✅ 好友私信</li>
            </ul>
          </div>
          <div class="border-2 border-purple-200 rounded-lg p-6 text-center bg-purple-50">
            <h3 class="text-xl font-bold text-purple-600 mb-2">年度订阅</h3>
            <p class="text-3xl font-bold mb-4">¥199<span class="text-sm font-normal">/年</span></p>
            <p class="text-xs text-purple-600 mb-2">省¥40.8</p>
            <ul class="text-sm text-gray-600 space-y-2 text-left">
              <li>✅ 全部新闻内容</li>
              <li>✅ 语音播报</li>
              <li>✅ 语言转译</li>
              <li>✅ 文件下载</li>
              <li>✅ 好友私信</li>
            </ul>
          </div>
          <div class="border-2 border-orange-200 rounded-lg p-6 text-center bg-orange-50">
            <h3 class="text-xl font-bold text-orange-600 mb-2">永久会员</h3>
            <p class="text-3xl font-bold mb-4">¥599<span class="text-sm font-normal">/永久</span></p>
            <p class="text-xs text-orange-600 mb-2">最划算</p>
            <ul class="text-sm text-gray-600 space-y-2 text-left">
              <li>✅ 全部新闻内容</li>
              <li>✅ 语音播报</li>
              <li>✅ 语言转译</li>
              <li>✅ 文件下载</li>
              <li>✅ 好友私信</li>
              <li>✅ 终身更新</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-lg p-8 mb-8">
        <h2 class="text-2xl font-bold mb-4">⚖️ 法律文档</h2>
        <div class="grid md:grid-cols-3 gap-4">
          <div class="border border-gray-200 rounded-lg p-4">
            <h3 class="font-semibold mb-2">📜 用户协议</h3>
            <p class="text-sm text-gray-600">5万字以上</p>
            <p class="text-xs text-gray-500 mt-2">十篇完整内容</p>
          </div>
          <div class="border border-gray-200 rounded-lg p-4">
            <h3 class="font-semibold mb-2">🔒 隐私政策</h3>
            <p class="text-sm text-gray-600">5万字以上</p>
            <p class="text-xs text-gray-500 mt-2">详细保护措施</p>
          </div>
          <div class="border border-gray-200 rounded-lg p-4">
            <h3 class="font-semibold mb-2">🍪 Cookie政策</h3>
            <p class="text-sm text-gray-600">使用询问</p>
            <p class="text-xs text-gray-500 mt-2">功能/分析/营销</p>
          </div>
        </div>
      </div>

      <div class="bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg shadow-lg p-8 text-white text-center">
        <h2 class="text-3xl font-bold mb-4">🚀 立即开始</h2>
        <p class="text-lg mb-6">注册账号，享受完整功能</p>
        <div class="flex justify-center gap-4">
          <NuxtLink to="/register" class="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition">
            立即注册
          </NuxtLink>
          <NuxtLink to="/news" class="bg-white bg-opacity-20 px-8 py-3 rounded-lg font-semibold hover:bg-opacity-30 transition">
            浏览新闻
          </NuxtLink>
        </div>
      </div>

      <div class="mt-12 text-center text-gray-500 text-sm">
        <p>© 2026 桂林市临桂区融媒体中心</p>
        <p class="mt-2">
          <strong>联系方式：</strong>service@lingui.cn | 0773-558XXXX
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
useHead({
  title: '临桂资讯 - 桂林市临桂区官方新闻资讯平台'
})
</script>
