# 自动从Google Scholar更新BibTeX文件

这个功能可以自动从Google Scholar抓取您的出版物并更新`pub.bib`文件。

## ⚠️ 重要说明

由于Google Scholar有反爬虫机制，自动抓取可能不够稳定。我们提供了两种方法：

### 方法1: 使用scholarly库（推荐尝试）

这是最简单的方法，但可能因为Google Scholar的反爬虫机制而不够稳定。

**设置步骤：**

1. **确保GitHub Secrets已配置**：
   - 在GitHub仓库的 `Settings -> Secrets -> Actions` 中
   - 确保有 `GOOGLE_SCHOLAR_ID` secret（如果还没有，请添加）
   - 值应该是您的Google Scholar ID（例如：`AUpqepUAAAAJ`）

2. **启用GitHub Actions**：
   - 在GitHub仓库的 `Actions` 标签页中
   - 点击 "I understand my workflows, go ahead and enable them"
   - 工作流会自动运行

3. **工作流触发方式**：
   - **自动触发**：每天08:00 UTC自动运行
   - **手动触发**：在Actions页面点击 "Update BibTeX from Google Scholar" -> "Run workflow"
   - **代码更新触发**：当相关脚本文件更新时自动运行

### 方法2: 手动导出后处理（最稳定）

如果自动抓取不稳定，您可以：

1. **从Google Scholar手动导出**：
   - 访问您的Google Scholar页面
   - 对于每篇论文，点击论文标题
   - 点击 "Cite" 按钮
   - 选择 "BibTeX" 格式
   - 复制BibTeX内容

2. **使用脚本合并**：
   ```bash
   python scripts/merge_bibtex.py new_entries.bib pub.bib
   ```

## 📝 自定义字段保留

脚本会智能合并新抓取的数据和现有的`pub.bib`文件：

- ✅ **保留自定义字段**：如 `corresponding`, `cofirst`, `category` 等
- ✅ **避免重复**：基于论文标题自动去重
- ✅ **格式统一**：自动标准化作者姓名格式

## 🔧 本地测试

如果想在本地测试脚本：

```bash
# 安装依赖
pip install -r scripts/requirements.txt

# 设置环境变量并运行
export GOOGLE_SCHOLAR_ID="AUpqepUAAAAJ"
export BIB_OUTPUT_FILE="pub.bib"
python scripts/fetch_google_scholar_bib.py
```

## ⚙️ 配置选项

在GitHub Actions工作流中，您可以：

1. **修改更新频率**：
   编辑 `.github/workflows/update-bibtex.yml`
   修改 `cron: '0 8 * * *'` 为其他时间

2. **禁用自动更新**：
   注释掉 `schedule` 部分，只保留 `workflow_dispatch`

## 🐛 故障排除

如果自动更新失败：

1. **检查GitHub Actions日志**：
   - 在Actions页面查看运行日志
   - 查找错误信息

2. **常见问题**：
   - **"scholarly library not installed"**: 确保requirements.txt包含所有依赖
   - **"No publications found"**: Google Scholar可能暂时无法访问，稍后重试
   - **"Rate limit exceeded"**: Google Scholar限制了访问频率，等待一段时间后重试

3. **备选方案**：
   - 使用手动导出方法
   - 或者等待Google Scholar的反爬虫限制解除后重试

## 📚 相关文件

- `scripts/fetch_google_scholar_bib.py`: 主要的抓取脚本
- `.github/workflows/update-bibtex.yml`: GitHub Actions工作流配置
- `scripts/requirements.txt`: Python依赖列表

