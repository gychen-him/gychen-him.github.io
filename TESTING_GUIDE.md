# 🧪 Google Scholar BibTeX 自动更新测试指南

## 📝 修复内容

已修复以下关键问题：
1. ✅ 正确点击 Cite 按钮而不是标题链接
2. ✅ 正确处理弹出的引用窗口
3. ✅ 正确切换和关闭新标签页
4. ✅ 添加详细的日志输出，便于调试
5. ✅ 改进错误处理和窗口管理

## 🔧 测试准备

### 1. 本地测试（推荐先做）

**安装依赖：**
```bash
pip install selenium bibtexparser
```

**安装 ChromeDriver：**

- **macOS:**
  ```bash
  brew install chromedriver
  ```

- **Linux (Ubuntu/Debian):**
  ```bash
  sudo apt-get update
  sudo apt-get install chromium-browser chromium-chromedriver
  ```

- **Windows:**
  1. 下载 ChromeDriver: https://chromedriver.chromium.org/
  2. 解压并添加到系统 PATH

**验证安装：**
```bash
chromedriver --version
# 应该显示版本号，例如：ChromeDriver 120.0.6099.109
```

### 2. 准备 Google 账号信息

**如果没有启用 2FA（双因素认证）：**
- 直接使用您的邮箱和密码

**如果启用了 2FA（推荐）：**
1. 访问：https://myaccount.google.com/apppasswords
2. 登录您的 Google 账号
3. 创建新的应用专用密码：
   - 选择应用：其他（自定义名称）
   - 输入名称：GitHub Scholar Bot
   - 点击生成
4. 复制生成的 16 位密码（例如：abcd efgh ijkl mnop）
5. 使用这个应用专用密码而不是您的主密码

## 🚀 开始测试

### 方法1: 本地测试（可以看到浏览器操作，便于调试）

**步骤1：设置环境变量**

在终端中运行：

```bash
# 设置您的 Google Scholar ID
export GOOGLE_SCHOLAR_ID="AUpqepUAAAAJ"

# 设置您的 Google 账号邮箱
export GOOGLE_EMAIL="your-email@gmail.com"

# 设置您的密码（或应用专用密码）
export GOOGLE_PASSWORD="your-password-here"

# 设置输出文件
export BIB_OUTPUT_FILE="pub_test.bib"

# 设置为非 headless 模式，可以看到浏览器操作
export HEADLESS="false"
```

**Windows (PowerShell):**
```powershell
$env:GOOGLE_SCHOLAR_ID="AUpqepUAAAAJ"
$env:GOOGLE_EMAIL="your-email@gmail.com"
$env:GOOGLE_PASSWORD="your-password-here"
$env:BIB_OUTPUT_FILE="pub_test.bib"
$env:HEADLESS="false"
```

**步骤2：运行脚本**

```bash
cd /Users/guangyongchen/Research/gychen-him.github.io
python scripts/fetch_google_scholar_bib_auth.py
```

**观察输出：**

您应该看到类似的日志：
```
Starting authenticated BibTeX fetch from Google Scholar...
Scholar ID: AUpqepUAAAAJ
Output file: pub_test.bib
Logging in to Google account...
Login successful!

============================================================
Fetching all publications for Scholar ID: AUpqepUAAAAJ
============================================================

📄 Page 1
------------------------------------------------------------
Found 20 publications on this page

[1/20] Processing: PhyloTune: a phylogeny-guided large language...
  → Found BibTeX link, clicking...
  → Successfully extracted BibTeX
  → Added 1 entry(ies)

[2/20] Processing: DivPro: Diverse protein sequence design...
  → Found BibTeX link, clicking...
  → Successfully extracted BibTeX
  → Added 1 entry(ies)

...

✓ Total extracted: 20 BibTeX entries

📊 Page summary: 20 entries extracted
📊 Running total: 20 entries

→ Loading next page...
```

**步骤3：检查结果**

如果成功，您会看到：
```
✓ Extraction complete: XX total entries
Successfully updated pub_test.bib with XX entries
```

检查生成的文件：
```bash
ls -lh pub_test.bib
head -50 pub_test.bib
```

### 方法2: 本地 Headless 测试（模拟 GitHub Actions 环境）

```bash
export GOOGLE_SCHOLAR_ID="AUpqepUAAAAJ"
export GOOGLE_EMAIL="your-email@gmail.com"
export GOOGLE_PASSWORD="your-password-here"
export BIB_OUTPUT_FILE="pub_test.bib"
export HEADLESS="true"  # headless 模式

python scripts/fetch_google_scholar_bib_auth.py
```

## 🌐 GitHub Actions 测试

### 步骤1：设置 GitHub Secrets

1. 访问您的仓库：https://github.com/gychen-him/gychen-him.github.io
2. 点击 `Settings` → `Secrets and variables` → `Actions`
3. 点击 `New repository secret`
4. 添加以下三个 secrets：

   **Secret 1:**
   - Name: `GOOGLE_SCHOLAR_ID`
   - Value: `AUpqepUAAAAJ`

   **Secret 2:**
   - Name: `GOOGLE_EMAIL`
   - Value: 您的 Google 邮箱

   **Secret 3:**
   - Name: `GOOGLE_PASSWORD`
   - Value: 您的密码或应用专用密码

### 步骤2：提交代码

```bash
cd /Users/guangyongchen/Research/gychen-him.github.io
git add scripts/fetch_google_scholar_bib_auth.py
git commit -m "Fix BibTeX extraction logic and improve error handling"
git push
```

### 步骤3：手动触发 GitHub Action

1. 访问：https://github.com/gychen-him/gychen-him.github.io/actions
2. 点击左侧的 "Update BibTeX from Google Scholar"
3. 点击右上角的 "Run workflow" 按钮
4. 选择 `main` 分支
5. 点击绿色的 "Run workflow" 按钮

### 步骤4：查看运行日志

1. 等待几秒，工作流开始运行
2. 点击新出现的运行记录
3. 点击 "update-bibtex" 任务
4. 查看各个步骤的日志，特别是：
   - "Install Chrome and ChromeDriver" - 确保安装成功
   - "Fetch BibTeX from Google Scholar" - 查看详细的抓取日志

## 🐛 常见问题排查

### 问题1: "Login failed"

**可能原因：**
- 邮箱或密码错误
- 需要使用应用专用密码（如果启用了 2FA）
- Google 检测到异常登录

**解决方案：**
1. 在本地非 headless 模式下测试，观察登录过程
2. 检查是否需要完成验证码或安全检查
3. 使用应用专用密码
4. 先在浏览器中正常登录一次 Google Scholar

### 问题2: "Could not find BibTeX link"

**可能原因：**
- Google Scholar 页面结构改变
- 网络延迟导致元素未加载

**解决方案：**
1. 在本地非 headless 模式下观察实际页面结构
2. 增加等待时间（修改脚本中的 `time.sleep()` 值）
3. 截图页面结构，我可以进一步调整选择器

### 问题3: "No publications found"

**可能原因：**
- Scholar ID 错误
- 账号未登录成功
- 页面加载失败

**解决方案：**
1. 确认 Scholar ID 正确：在您的 Google Scholar 页面 URL 中查找
2. 检查登录日志
3. 增加页面加载等待时间

### 问题4: Chrome/ChromeDriver 版本不匹配

**错误信息：**
```
session not created: This version of ChromeDriver only supports Chrome version XX
```

**解决方案：**
```bash
# macOS
brew upgrade chromedriver

# Linux
sudo apt-get update
sudo apt-get upgrade chromium-chromedriver

# 或手动下载匹配的版本
```

## 📊 成功标志

✅ **本地测试成功：**
- 看到 "Login successful!"
- 看到 "Successfully extracted BibTeX" 多次
- 生成了 `pub_test.bib` 文件
- 文件包含正确的 BibTeX 条目

✅ **GitHub Actions 成功：**
- 工作流状态显示绿色 ✓
- 日志中看到 "Successfully updated pub.bib"
- 仓库中的 `pub.bib` 文件已更新
- 有新的 commit: "Auto-update BibTeX from Google Scholar"

## 📝 测试反馈

测试后，请告诉我：
1. **成功了吗？** 如果成功，抓取了多少篇论文？
2. **遇到什么错误？** 复制完整的错误信息
3. **哪一步卡住了？** 登录、提取、还是其他？
4. **有截图吗？** 如果在本地非 headless 模式下，可以截图页面状态

## 🔄 下一步

**如果测试成功：**
1. 可以让它每天自动运行（已配置为每天 08:00 UTC）
2. 或者每次更新论文后手动触发
3. 保持您的自定义字段（corresponding, cofirst, category）

**如果测试失败：**
1. 提供错误日志
2. 我会根据具体错误调整代码
3. 可能需要尝试其他方案（代理、批量导出等）

