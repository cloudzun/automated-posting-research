# 所需资源和依赖项

## 外部服务要求

### 1. 代理服务
- **目的**: IP轮换以避免检测
- **推荐提供商**:
  - Bright Data (前身为Luminati)
  - Smartproxy
  - Oxylabs
  - NetNut
- **要求**:
  - 住宅代理优先
  - 最少50-100个代理池
  - 全球地理分布
  - 99%以上正常运行时间SLA
- **预计费用**: $100-500/月

### 2. 验证码解决服务
- **目的**: 自动验证码解决
- **推荐提供商**:
  - 2captcha
  - Anti-Captcha
  - CapMonster Cloud
- **要求**:
  - reCAPTCHA v2/v3 支持
  - 图片验证码解决
  - API集成能力
  - 高成功率 (>95%)
- **预计费用**: $20-100/月 (取决于量级)

### 3. 临时邮箱服务
- **目的**: 账户验证
- **推荐选项**:
  - Guerrilla Mail (免费API)
  - Temp Mail API
  - 10 Minute Mail API
- **要求**:
  - 编程访问
  - 邮件检索能力
  - 链接提取功能

### 4. 基础设施
- **托管**: 云VPS (AWS/GCP/DigitalOcean)
- **要求**:
  - 专用IP地址
  - 足够RAM用于浏览器实例
  - 可靠互联网连接
  - 支持Chrome/Chromium
- **预计费用**: $20-100/月

## 软件依赖

### 运行环境
- Python 3.8+
- Chrome/Chromium浏览器
- ChromeDriver
- Selenium WebDriver
- Requests库
- Undetected ChromeDriver (用于隐身)

### 开发库
- selenium
- requests
- undetected-chromedriver
- webdriver-manager
- python-dotenv

## 安全和隐私考虑
- 加密凭证存储
- 安全通信协议
- 数据保留政策
- 平台服务条款合规